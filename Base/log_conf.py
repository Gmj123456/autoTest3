# 日志配置import logging
from pathlib import Path
import datetime

def setup_logging():
    """统一日志配置"""
    log_dir = Path(__file__).parent.parent / 'logs'
    log_dir.mkdir(exist_ok=True)
    
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # 防止重复添加handler
    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # 文件处理器，使用时间戳生成唯一的文件名
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    file_handler = logging.FileHandler(log_dir / f'automation_{timestamp}.log', encoding='utf-8')
    file_handler.setFormatter(formatter)
    
    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # 添加第三方库日志过滤
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('selenium').setLevel(logging.WARNING)

    return logger