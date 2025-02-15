import json
import yaml
from pathlib import Path
import os
import sys

def get_resource_path(relative_path):
    """获取资源文件的绝对路径（支持 PyInstaller 打包）"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class Translator:
    """国际化翻译器
    
    配置说明：
    1. 语言设置：从 config.yaml 的 language 字段读取
    2. 翻译文件：从 i18n/{language}.json 读取
    3. 翻译规则：使用键值对映射，找不到键时返回原文
    
    用法示例：
    translator = Translator()
    text = translator.translate("key")  # 返回对应语言的文本
    """
    def __init__(self):
        config_path = get_resource_path('config.yaml')
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        lang_file = get_resource_path(f"i18n/{config['language']}.json")
        with open(lang_file, 'r', encoding='utf-8') as f:
            self.translations = json.load(f)
    
    def translate(self, key, lang='zh_CN'):
        return self.translations.get(key, key)  # 简化了参数，直接使用配置文件中的语言