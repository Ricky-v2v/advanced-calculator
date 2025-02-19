# 在文件顶部添加
import sys
import os
from src.utils.logger import setup_logger
from src.i18n.translator import Translator
from src.utils.version_checker import check_update
import math
import re
import json
import yaml  # 添加这行
from pathlib import Path
from functools import wraps
from collections import deque
from datetime import datetime

# 配置常量
HISTORY_FILE = "calc_history.json"  # 历史记录文件路径
MAX_MEMORY_HISTORY = 10            # 内存中保存的最大历史记录数
MAX_DISPLAY_HISTORY = 5            # 显示的最大历史记录数

# 颜色配置（跨平台兼容）
# Windows 系统需要初始化 colorama
# 如果导入失败，使用空字符串替代颜色代码
try:
    from colorama import init, Fore, Style
    init(autoreset=True)
except ImportError:
    class FakeColors:
        def __getattr__(self, name):
            return ''
    Fore = Style = FakeColors()

# ======================
# 装饰器定义
# ======================
def handle_errors(func):
    """统一错误处理装饰器
    
    处理两种场景：
    1. 测试模式：重新抛出异常以便测试捕获
    2. 正常模式：打印友好的错误信息
    
    参数：
        func: 被装饰的函数
    
    返回：
        wrapper: 包装后的函数
    """
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValueError, Exception) as e:
            # 在测试模式下重新抛出异常
            if 'unittest' in sys.modules:
                raise
            # 在正常模式下打印错误信息
            print(f"{Fore.RED}错误: {str(e)}{Style.RESET_ALL}")
    return wrapper

# 


# ======================
# 类定义
# ======================
class HistoryManager:
    """历史记录管理器
    
    功能：
    1. 内存中保存最近的计算记录
    2. 将历史记录持久化到文件
    3. 从文件加载历史记录
    4. 支持获取最近的记录
    
    属性：
        memory_history (deque): 内存中的历史记录队列
        history_file (Path): 历史记录文件路径
    """
    
    def __init__(self):
        self.memory_history = deque(maxlen=MAX_MEMORY_HISTORY)
        self.history_file = Path(HISTORY_FILE)
        # 确保历史文件存在
        if not self.history_file.exists():
            self.history_file.touch()
        self.load_history()

    def add_record(self, record):
        """添加新记录"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{timestamp}] {record}"
        self.memory_history.append(entry)
        self.save_history()

    def get_recent_history(self):
        """获取最近的记录"""
        return list(self.memory_history)[-MAX_DISPLAY_HISTORY:]

    def save_history(self):
        """保存历史到文件"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(list(self.memory_history), f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"{Fore.YELLOW}警告: 无法保存历史记录 - {str(e)}{Style.RESET_ALL}")

    def load_history(self):
        """从文件加载历史
        
        加载规则：
        1. 检查历史文件是否存在
        2. 从 JSON 文件读取历史记录
        3. 只保留最近的 MAX_MEMORY_HISTORY 条记录
        4. 加载失败时显示警告但不中断程序
        """
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r') as f:
                    history = json.load(f)
                    self.memory_history.extend(history[-MAX_MEMORY_HISTORY:])
            except Exception as e:
                print(f"{Fore.YELLOW}警告: 无法加载历史记录 - {str(e)}{Style.RESET_ALL}")

class CalculatorCore:
    """计算器核心逻辑
    
    提供以下功能：
    1. 基本运算：+, -, *, /, ^, %
    2. 科学函数：sqrt, sin, cos, tan, log, log10, abs
    3. 复数运算：+c, -c, *c, /c, abs_c, real, imag
    
    属性：
        FUNCTIONS (dict): 支持的数学函数映射
        OPERATORS (dict): 支持的运算符映射
    """
    
    # 函数映射格式：
    # 'func_name': (function, arg_count, validator, error_message)
    # - function: 实际的函数实现
    # - arg_count: 参数个数
    # - validator: 参数验证函数
    # - error_message: 验证失败时的错误信息
    FUNCTIONS = {
        'sqrt': (math.sqrt, 1, lambda x: x >= 0, "error.negative_sqrt"),
        'sin': (math.sin, 1, lambda _: True, ""),
        'cos': (math.cos, 1, lambda _: True, ""),
        'tan': (math.tan, 1, lambda x: x % 90 != 0, "error.invalid_tan"),
        'log': (math.log, 1, lambda x: x > 0, "error.positive_required"),
        'log10': (math.log10, 1, lambda x: x > 0, "error.positive_required"),
        'abs': (abs, 1, lambda _: True, "")
    }
    
    # 添加基本运算符映射
    OPERATORS = {
        '+': lambda a, b: a + b,
        '-': lambda a, b: a - b,
        '*': lambda a, b: a * b,
        '/': lambda a, b: a / b if b != 0 else raise_(ValueError("error.division_by_zero")),
        '%': lambda a, b: a % b if b != 0 else raise_(ValueError("error.division_by_zero")),
        '^': lambda a, b: a ** b,
    }
    
    def __init__(self, translator):
        self.translator = translator
        # 添加复数运算符
        self.OPERATORS.update({
            '+c': lambda a, b: complex(a) + complex(b),
            '-c': lambda a, b: complex(a) - complex(b),
            '*c': lambda a, b: complex(a) * complex(b),
            '/c': lambda a, b: complex(a) / complex(b) if b != 0 else raise_(ValueError(self.translator.translate("error.division_by_zero")))
        })
        
        self.FUNCTIONS.update({
            'abs_c': (abs, 1, lambda x: isinstance(x, complex), self.translator.translate("error.complex_required")),
            'real': (lambda x: x.real, 1, lambda x: isinstance(x, complex), self.translator.translate("error.complex_required")),
            'imag': (lambda x: x.imag, 1, lambda x: isinstance(x, complex), self.translator.translate("error.complex_required"))
        })
    
    @handle_errors
    def calculate(self, num1, num2, operator):
        """执行二元运算
        
        参数：
            num1 (float): 第一个操作数
            num2 (float): 第二个操作数
            operator (str): 运算符，必须在 OPERATORS 中定义
        
        返回：
            float: 运算结果
            
        异常：
            ValueError: 当运算符不支持或运算无效（如除零）时抛出
        """
        if operator not in self.OPERATORS:
            raise ValueError(f"不支持的运算符: {operator}")
        return self.OPERATORS[operator](num1, num2)
    
    @handle_errors
    def process_function(self, func_name, value):
        """处理函数调用
        
        支持的函数：
        - 三角函数：sin, cos, tan（输入为角度）
        - 数学函数：sqrt, log, log10, abs
        """
        if func_name not in self.FUNCTIONS:
            raise ValueError(f"不支持的函数: {func_name}")
            
        func, _, validator, error_msg = self.FUNCTIONS[func_name]
        if not validator(value):
            raise ValueError(error_msg)
            
        if func_name in ('sin', 'cos', 'tan'):
            # 将角度转换为弧度
            value = math.radians(value)
            
        return func(value)

# 在类外添加辅助函数
def raise_(ex):
    """辅助函数：用于在 lambda 中抛出异常"""
    raise ex

class CalculatorUI:
    """用户界面处理类
    
    功能：
    1. 命令行交互界面
    2. 命令自动补全
    3. 多行输入支持
    4. 帮助信息显示
    
    属性：
        core (CalculatorCore): 计算器核心实例
        history (HistoryManager): 历史记录管理器实例
    """
    def __init__(self, core, history, translator):  # 添加 translator 参数
        self.core = core
        self.history = history
        self.translator = translator  # 保存翻译器实例
        self.setup_autocomplete()

    def setup_autocomplete(self):
        """设置自动完成（如果可用）"""
        try:
            import readline
            readline.parse_and_bind("tab: complete")
            readline.set_completer(self.autocomplete)
        except ImportError:
            pass

    def autocomplete(self, text, state):
        """自动完成逻辑"""
        options = [f"{k}(" for k in CalculatorCore.FUNCTIONS.keys() if k.startswith(text)]
        options += [op for op in CalculatorCore.OPERATORS.keys() if op.startswith(text)]
        return (options + [None])[state]

    def display_help(self):
        """显示帮助信息"""
        print(f"\n{Fore.CYAN}{self.translator.translate('help_title')}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{self.translator.translate('basic_ops')}: {Style.RESET_ALL}3 + 5, 2.5e3 * -1.5")
        print(f"{Fore.GREEN}{self.translator.translate('func_call')}: {Style.RESET_ALL}sin(30), log(100), sqrt(25)")
        print(f"{Fore.GREEN}{self.translator.translate('complex_ops')}: {Style.RESET_ALL}1 +c 2j, 3 *c (1+2j)")
        print(f"{Fore.GREEN}{self.translator.translate('supported_funcs')}: {Style.RESET_ALL}{', '.join(CalculatorCore.FUNCTIONS.keys())}")
        print(f"{Fore.GREEN}{self.translator.translate('commands')}: {Style.RESET_ALL}")
        print(f"  q - {self.translator.translate('exit')}  h - {self.translator.translate('help')}  c - {self.translator.translate('clear')}  l - {self.translator.translate('history')}  m - {self.translator.translate('multiline')}")

    def get_expression(self):
        print(f"{Fore.YELLOW}{self.translator.translate('multiline_prompt')}{Style.RESET_ALL}")
        lines = []
        while True:
            line = input("> ").strip()
            if not line and lines:
                break
            if line.lower() in ('q', 'h', 'c', 'l', 'm'):
                return line.lower()
            lines.append(line)
        return ' '.join(lines).replace('\n', ' ')

# ======================
# 主程序
# ======================
"""
高级科学计算器命令行界面
提供基本运算、科学函数计算、复数运算等功能
支持历史记录、多行输入、自动补全等特性

主要组件：
- CalculatorCore: 核心计算逻辑
- CalculatorUI: 用户界面处理
- HistoryManager: 历史记录管理
- ScientificCalculator: 主程序入口
"""

def get_resource_path(relative_path):
    """获取资源文件的绝对路径（支持 PyInstaller 打包）"""
    try:
        # PyInstaller 创建临时文件夹 _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class ScientificCalculator:
    def __init__(self):
        try:
            # 设置翻译器（移到最前面）
            self.translator = Translator()
            
            # 加载配置
            config_path = get_resource_path('config.yaml')
            with open(config_path, 'r') as f:
                self.config = yaml.safe_load(f)
            
            # 设置日志
            self.logger = setup_logger()
            
            # 检查更新
            try:
                has_update, latest_version = check_update()
                if has_update:
                    print(f"{Fore.YELLOW}{self.translator.translate('update_available')}: {latest_version}{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.YELLOW}{self.translator.translate('error.update_check_failed')}: {str(e)}{Style.RESET_ALL}")
            
            # 初始化其他组件
            self.history = HistoryManager()
            self.core = CalculatorCore(self.translator)
            self.ui = CalculatorUI(self.core, self.history, self.translator)
            
        except Exception as e:
            print(f"{Fore.RED}{self.translator.translate('error.init_failed')}: {str(e)}{Style.RESET_ALL}")
            sys.exit(1)

    def run(self):
        print(f"{Fore.BLUE}{self.translator.translate('welcome')}{Style.RESET_ALL}")
        # 修改这里的硬编码中文
        multi_line_mode = False

        while True:
            try:
                expr = self.ui.get_expression() if multi_line_mode else \
                    input(f"\n{self.translator.translate('prompt')}").strip()

                if not expr:
                    continue

                # 处理命令
                if expr == 'q':
                    break
                if expr == 'h':
                    self.ui.display_help()
                    continue
                if expr == 'c':
                    print("\n" * 50)
                    continue
                if expr == 'l':
                    self.show_history()
                    continue
                if expr == 'm':
                    multi_line_mode = not multi_line_mode
                    print(self.translator.translate('multiline_enabled' if multi_line_mode else 'multiline_disabled'))
                    continue

                # 解析和执行表达式
                result, record = self.process_expression(expr)
                if result is not None:
                    print(f"{Fore.GREEN}{self.translator.translate('result')}: {result:.6g}{Style.RESET_ALL}")
                    self.history.add_record(record)

            except KeyboardInterrupt:
                print("\n检测到退出请求...")
                break

    def process_expression(self, expr):
        """处理表达式并返回结果
        
        支持的表达式格式：
        1. 函数调用：sin(30), log(100)
        2. 基本运算：2+3, 5*6
        3. 复数运算：(1+2j)+(2+3j), (2+3j)*(1+1j)
        """
        expr = expr.strip()
        
        # 匹配函数调用
        func_match = re.match(r"^([a-z_]+)\((.*)\)$", expr)
        if func_match:
            func_name, arg = func_match.groups()
            try:
                # 尝试解析复数参数
                arg = complex(arg) if 'j' in arg else float(arg)
                result = self.core.process_function(func_name, arg)
                return result, f"{func_name}({arg})={result:.6g}"
            except ValueError:
                pass
    
        # 匹配复数运算
        complex_match = re.match(r"^\((.*?)\)\s*([+\-*/])\s*\((.*?)\)$", expr)
        if complex_match:
            try:
                num1, op, num2 = complex_match.groups()
                num1 = complex(num1)
                num2 = complex(num2)
                if isinstance(num1, complex) or isinstance(num2, complex):
                    result = self.core.calculate(num1, num2, f"{op}c")
                    return result, f"({num1}){op}({num2})={result}"
            except ValueError:
                pass
    
        # 匹配基本运算
        basic_match = re.match(r"^([+-]?\d+\.?\d*(?:e[+-]?\d+)?)([+\-*/%^])([+-]?\d+\.?\d*(?:e[+-]?\d+)?)$", expr)
        if basic_match:
            num1, op, num2 = basic_match.groups()
            result = self.core.calculate(float(num1), float(num2), op)
            return result, f"{num1}{op}{num2}={result}"

        raise ValueError("无法识别的表达式格式")

    def show_history(self):
        """显示历史记录"""
        print(f"\n{self.translator.translate('recent_calculations')}")
        for i, record in enumerate(self.history.get_recent_history(), 1):
            print(f"{i}. {record}")
        print()

if __name__ == "__main__":
    os.environ['LANG'] = 'en_US'
    ScientificCalculator().run()
    