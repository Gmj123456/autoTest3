import base64
import requests
import sys
import logging
from pathlib import Path



class BaiduOCR:
    def __init__(self, api_key, secret_key):
        self.api_key = api_key
        self.secret_key = secret_key
        self.access_token = None
        self.setup_logging()
        self.get_initial_access_token()

    def setup_logging(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def get_initial_access_token(self):
        self.access_token = self.get_access_token()
        if not self.access_token:
            logging.error("无法获取初始 access_token，程序退出。")
            sys.exit(1)

    def get_access_token(self):
        auth_url = f"https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={self.api_key}&client_secret={self.secret_key}"
        try:
            logging.info(f"请求 access_token 的 URL: {auth_url}")
            response = requests.get(auth_url, timeout=10)
            response.raise_for_status()
            result = response.json()
            access_token = result.get('access_token')
            if access_token:
                logging.info("成功获取 access_token")
                return access_token
            else:
                logging.error("未从响应中获取到 access_token，响应内容: %s", result)
        except requests.RequestException as e:
            logging.error("请求 access_token 时出现网络异常: %s", e)
        except ValueError as e:
            logging.error("解析 access_token 响应的 JSON 数据时出错: %s", e)
        return None

    def read_image(self, image_path):
        try:
            with open(image_path, 'rb') as f:
                return base64.b64encode(f.read())
        except FileNotFoundError:
            logging.error("未找到图片文件 '%s'", image_path)
            return None

    def send_ocr_request(self, request_url, access_token, image):
        full_request_url = f"{request_url}?access_token={access_token}"
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        params = {"image": image}
        try:
            response = requests.post(full_request_url, data=params, headers=headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logging.error("文字识别请求时出现网络异常: %s", e)
        except ValueError as e:
            logging.error("解析文字识别响应的 JSON 数据时出错: %s", e)
        return None

    def process_ocr_response(self, response):
        if response is None:
            return None, None
        if 'error_code' in response:
            if response['error_code'] in [110, 111]:
                return None, response
            logging.error("文字识别请求出错，错误码: %s，错误信息: %s", response['error_code'], response['error_msg'])
        else:
            try:
                result = response['words_result'][0]['words']
                logging.info("识别结果: %s", result)
                return result, None
            except (KeyError, IndexError):
                logging.error("解析文字识别响应结果时出错，请检查响应数据格式。完整的响应数据: %s", response)
        return None, None

    def ocr_accurate_basic(self, image_path):
        request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"
        image = self.read_image(image_path)
        if image is None:
            return None

        access_token = self.access_token
        for _ in range(2):
            response = self.send_ocr_request(request_url, access_token, image)
            result, error_response = self.process_ocr_response(response)
            if result is not None:
                return result
            if error_response and error_response['error_code'] in [110, 111]:
                logging.warning("access_token %s，重新获取...",
                                "无效" if error_response['error_code'] == 110 else "过期")
                access_token = self.get_access_token()
                if access_token is None:
                    break
            else:
                break
        return None


def load_config():
    try:
        project_root = Path(__file__).resolve().parent.parent.parent
        sys.path.insert(0, str(project_root))
        
        # 保留动态导入（第114行）
        from Base.config import API_KEY, SECRET_KEY
        return API_KEY, SECRET_KEY
    except ImportError as e:
        logging.error(f"配置导入失败，请检查：{project_root}/Base/config.py 是否存在且包含API_KEY/SECRET_KEY")
        logging.error(f"完整错误信息：{str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    api_key, secret_key = load_config()
    ocr_client = BaiduOCR(api_key, secret_key)
    
    # 注释测试模式
    # if len(sys.argv) > 1 and sys.argv[1] == "--test":
    #     print("\n正在执行OCR功能测试...")
    #     test_result = ocr_client.test_ocr_functionality()
    #     sys.exit(0 if test_result else 1)
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        result = ocr_client.ocr_accurate_basic(image_path)
        if result is not None:
            print(result)
    else:
        logging.warning("请提供图片路径作为参数。")
