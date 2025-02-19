import requests
import yaml
import os
from pathlib import Path

def get_current_version():
    """获取当前版本号"""
    try:
        config_path = os.path.join(os.path.dirname(__file__), '..', 'config.yaml')
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
            return config.get('version', '1.0.0')
    except Exception:
        return '1.0.0'

def check_update():
    """检查更新
    
    返回：
        tuple: (是否有更新, 最新版本号)
    """
    try:
        current_version = get_current_version()
        # 这里可以实现实际的版本检查逻辑
        # 例如：从服务器获取最新版本号
        latest_version = current_version  # 暂时返回当前版本
        return False, latest_version
    except Exception as e:
        return False, None