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
        self.translations = {
            'welcome': 'Advanced Scientific Calculator (Enter \'h\' for help)',
            'prompt': 'Enter expression (or command): ',
            'help_title': 'Help Information',
            'basic_ops': 'Basic Operations',
            'func_call': 'Function Call',
            'complex_ops': 'Complex Operations',
            'supported_funcs': 'Supported Functions',
            'commands': 'Commands',
            'result': 'Result',
            'exit': 'Exit',
            'help': 'Help',
            'clear': 'Clear',
            'history': 'History',
            'multiline': 'Multi-line',
            'multiline_enabled': 'Multi-line mode enabled',
            'multiline_disabled': 'Multi-line mode disabled',
            'error': {
                'division_by_zero': 'Division by zero',
                'invalid_expression': 'Invalid expression format',
                'init_failed': 'Initialization failed'
            }
        }
        
        try:
            lang = os.environ.get('LANG', 'en_US').split('.')[0]
            i18n_path = self.get_resource_path(f'src/i18n/{lang}.json')
            if os.path.exists(i18n_path):
                with open(i18n_path, 'r', encoding='utf-8') as f:
                    self.translations.update(json.load(f))
        except Exception as e:
            print(f"Warning: Unable to load translation file, using defaults - {str(e)}")

    def get_resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    def translate(self, key):
        keys = key.split('.')
        value = self.translations
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return key
        return str(value)