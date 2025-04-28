from pathlib import Path
project_root = Path(__file__).parent.parent

# 指定chromedriver.exe路径
CHROME_DRIVER_PATH = project_root / 'Base'/ 'utils' / 'chromedriver.exe'

# ERP_URL = "http://192.168.150.222:3066"  # 本地环境
# LOGIN_SUCCESS_URL = "http://192.168.150.222:3066/dashboard/analysis"

ERP_URL = "http://124.222.178.125:3006"  # 测试环境
LOGIN_SUCCESS_URL = "http://124.222.178.125:3006/dashboard/analysis"

USERNAME = "guomj"  # 主测试账号
PASSWORD = "gmj123.."

PTUSER_NAME = "ptuser"  # 特殊账号
PTUSER_PASSWORD = "que123"

# ocr识别
API_KEY = '5mPZWWtbEIcYzeFKmhpQ0Cat'
SECRET_KEY = 'GBd6NyH5oBqXzrZfkyAsKSChKlZEMMTk'