import logging
import yaml
from pathlib import Path

def setup_logger():
    """设置日志记录器
    
    配置说明：
    1. 日志级别：从 config.yaml 的 logging.level 读取
    2. 日志文件：从 config.yaml 的 logging.file 读取
    3. 日志格式：时间 - 名称 - 级别 - 消息
    
    返回：
        Logger: 配置好的日志记录器实例
    """
    with open('config.yaml', 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)

    logger = logging.getLogger('calculator')
    logger.setLevel(config['logging']['level'])

    # 文件处理器
    fh = logging.FileHandler(config['logging']['file'], encoding='utf-8')
    fh.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))
    logger.addHandler(fh)

    return logger

def setup_logger():
    logger = logging.getLogger('calculator')
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger