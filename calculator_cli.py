# 在文件顶部添加
import sys
import os
from utils.logger import setup_logger
from i18n.translator import Translator
from utils.version_checker import check_update
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
        'sqrt': (math.sqrt, 1, lambda x: x >= 0, "负数不能开平方"),
        'sin': (lambda x: math.sin(math.radians(x)), 1, lambda _: True, ""),
        'cos': (lambda x: math.cos(math.radians(x)), 1, lambda _: True, ""),
        'tan': (lambda x: math.tan(math.radians(x)), 1, lambda x: x % 90 != 0, "角度不能是90的奇数倍"),
        'log': (math.log, 1, lambda x: x > 0, "需要正数参数"),
        'log10': (math.log10, 1, lambda x: x > 0, "需要正数参数"),
        'abs': (abs, 1, lambda _: True, "")
    }
    
    # 运算符映射格式：
    # 'operator': lambda a, b: operation(a, b)
    # 对于需要异常处理的操作，使用条件表达式和 raise_ 函数
    OPERATORS = {
        '+': lambda a, b: a + b,
        '-': lambda a, b: a - b,
        '*': lambda a, b: a * b,
        '/': lambda a, b: a / b if b != 0 else raise_(ValueError("除数不能为零")),
        '^': lambda a, b: a ** b,
        '%': lambda a, b: a % b if b != 0 else raise_(ValueError("取模运算的除数不能为零"))
    }

    def __init__(self):
        # 添加复数运算支持
        self.OPERATORS.update({
            '+c': lambda a, b: complex(a) + complex(b),
            '-c': lambda a, b: complex(a) - complex(b),
            '*c': lambda a, b: complex(a) * complex(b),
            '/c': lambda a, b: complex(a) / complex(b) if b != 0 else raise_(ValueError("除数不能为零"))
        })
        
        self.FUNCTIONS.update({
            'abs_c': (abs, 1, lambda x: isinstance(x, complex), "需要复数参数"),
            'real': (lambda x: x.real, 1, lambda x: isinstance(x, complex), "需要复数参数"),
            'imag': (lambda x: x.imag, 1, lambda x: isinstance(x, complex), "需要复数参数")
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
    def process_function(self, func_name, param):
        """处理数学函数"""
        if func_name not in self.FUNCTIONS:
            raise ValueError(f"不支持的函数: {func_name}")
        
        func, arg_count, validator, err_msg = self.FUNCTIONS[func_name]
        if arg_count != 1:
            raise ValueError("暂不支持多参数函数")
        
        if not validator(param):
            raise ValueError(err_msg or "参数验证失败")
        
        return func(param)

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
    def __init__(self, core, history):
        self.core = core
        self.history = history
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
        print(f"\n{Fore.CYAN}帮助信息:{Style.RESET_ALL}")
        print(f"{Fore.GREEN}基本运算:{Style.RESET_ALL} 3 + 5, 2.5e3 * -1.5")
        print(f"{Fore.GREEN}函数调用:{Style.RESET_ALL} sin(30), log(100), sqrt(25)")
        print(f"{Fore.GREEN}复数运算:{Style.RESET_ALL} 1 +c 2j, 3 *c (1+2j)")
        print(f"{Fore.GREEN}支持函数:{Style.RESET_ALL} {', '.join(CalculatorCore.FUNCTIONS.keys())}")
        print(f"{Fore.GREEN}命令:{Style.RESET_ALL}")
        print("  q - 退出  h - 帮助  c - 清屏  l - 历史  m - 多行模式")

    def get_expression(self):
        """获取用户输入（支持多行）
        
        输入处理规则：
        1. 单行模式：直接返回输入的表达式
        2. 多行模式：
           - 空行表示输入结束
           - 合并所有行并去除多余空格
        3. 命令处理：
           - 检查是否是特殊命令(q,h,c,l,m)
           - 是命令则直接返回命令字符
        
        返回：
            str: 处理后的表达式或命令
        """
        print(f"{Fore.YELLOW}输入表达式（输入空行结束多行输入）:{Style.RESET_ALL}")
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
            # 加载配置
            config_path = get_resource_path('config.yaml')
            with open(config_path, 'r') as f:
                self.config = yaml.safe_load(f)
            
            # 设置日志
            self.logger = setup_logger()
            
            # 设置翻译器
            self.translator = Translator()
            
            # 检查更新
            try:
                has_update, latest_version = check_update()
                if has_update:
                    print(f"发现新版本：{latest_version}")
            except Exception as e:
                print(f"{Fore.YELLOW}警告: 更新检查失败 - {str(e)}{Style.RESET_ALL}")
            
            # 初始化其他组件
            self.history = HistoryManager()
            self.core = CalculatorCore()
            self.ui = CalculatorUI(self.core, self.history)
            
        except Exception as e:
            print(f"{Fore.RED}初始化失败: {str(e)}{Style.RESET_ALL}")
            sys.exit(1)

    def run(self):
        """运行计算器主循环
        
        主循环处理流程：
        1. 输入处理：
           - 多行模式：使用 get_expression 获取多行输入
           - 单行模式：直接获取单行输入
        
        2. 命令处理：
           - q: 退出程序
           - h: 显示帮助
           - c: 清屏
           - l: 显示历史
           - m: 切换多行模式
        
        3. 表达式处理：
           - 解析表达式
           - 执行计算
           - 显示结果
           - 记录历史
        
        4. 异常处理：
           - 捕获键盘中断（Ctrl+C）
           - 优雅退出
        """
        print(f"{Fore.BLUE}高级科学计算器（输入 'h' 查看帮助）{Style.RESET_ALL}")
        multi_line_mode = False

        while True:
            try:
                expr = self.ui.get_expression() if multi_line_mode else \
                    input("\n输入表达式（或命令）: ").strip()

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
                    print(f"多行模式 {'已启用' if multi_line_mode else '已关闭'}")
                    continue

                # 解析和执行表达式
                result, record = self.process_expression(expr)
                if result is not None:
                    print(f"{Fore.GREEN}结果: {result:.6g}{Style.RESET_ALL}")
                    self.history.add_record(record)

            except KeyboardInterrupt:
                print("\n检测到退出请求...")
                break

    def process_expression(self, expr):
        # 清理输入并解析
        expr = re.sub(r'\s+', ' ', expr).strip()

        # 尝试匹配函数调用
        if func_match := re.match(r"^([a-z]+)\(?([+-]?\d+\.?\d*(?:e[+-]?\d+)?(?:[+-]?\d*\.?\d*j)?)\)?$", expr, re.I):
            func_name, param = func_match.groups()
            try:
                param = complex(param) if 'j' in param else float(param)
            except ValueError:
                raise ValueError("无效的参数格式")
            result = self.core.process_function(func_name.lower(), param)
            return result, f"{func_name}({param}) = {result:.6g}"

        # 尝试匹配二元运算
        if bin_match := re.match(r"^([+-]?\d+\.?\d*(?:e[+-]?\d+)?(?:[+-]?\d*\.?\d*j)?)([+\-*/%^c])([+-]?\d+\.?\d*(?:e[+-]?\d+)?(?:[+-]?\d*\.?\d*j)?)$", expr, re.I):
            num1_str, operator, num2_str = bin_match.groups()
            try:
                num1 = complex(num1_str) if 'j' in num1_str else float(num1_str)
                num2 = complex(num2_str) if 'j' in num2_str else float(num2_str)
            except ValueError:
                raise ValueError("无效的数字格式")
            result = self.core.calculate(num1, num2, operator)
            return result, f"{num1_str}{operator}{num2_str}={result:.6g}"

        raise ValueError("无法识别的表达式格式")

    def show_history(self):
        """显示历史记录"""
        print(f"\n{Fore.CYAN}最近计算记录:{Style.RESET_ALL}")
        for idx, item in enumerate(self.history.get_recent_history(), 1):
            print(f"{Fore.YELLOW}{idx}.{Style.RESET_ALL} {item}")

if __name__ == "__main__":
    ScientificCalculator().run()
    