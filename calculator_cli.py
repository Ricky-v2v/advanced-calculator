import math
import re
import json
from pathlib import Path
from functools import wraps
from collections import deque
from datetime import datetime

# 配置常量
HISTORY_FILE = "calc_history.json"
MAX_MEMORY_HISTORY = 10
MAX_DISPLAY_HISTORY = 5

# 颜色配置（跨平台兼容）
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
    """统一错误处理装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            print(f"{Fore.RED}错误: {str(e)}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}系统错误: {str(e)}{Style.RESET_ALL}")
    return wrapper

# ======================
# 类定义
# ======================
class HistoryManager:
    """历史记录管理器"""
    def __init__(self):
        self.memory_history = deque(maxlen=MAX_MEMORY_HISTORY)
        self.history_file = Path(HISTORY_FILE)
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
            with open(self.history_file, 'w') as f:
                json.dump(list(self.memory_history), f)
        except Exception as e:
            print(f"{Fore.YELLOW}警告: 无法保存历史记录 - {str(e)}{Style.RESET_ALL}")

    def load_history(self):
        """从文件加载历史"""
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r') as f:
                    history = json.load(f)
                    self.memory_history.extend(history[-MAX_MEMORY_HISTORY:])
            except Exception as e:
                print(f"{Fore.YELLOW}警告: 无法加载历史记录 - {str(e)}{Style.RESET_ALL}")

class CalculatorCore:
    """计算器核心逻辑"""
    FUNCTIONS = {
        'sqrt': (math.sqrt, 1, lambda x: x >= 0, "负数不能开平方"),
        'sin': (lambda x: math.sin(math.radians(x)), 1, lambda _: True, ""),
        'cos': (lambda x: math.cos(math.radians(x)), 1, lambda _: True, ""),
        'tan': (lambda x: math.tan(math.radians(x)), 1, lambda x: x % 90 != 0, "角度不能是90的奇数倍"),
        'log': (math.log, 1, lambda x: x > 0, "需要正数参数"),
        'log10': (math.log10, 1, lambda x: x > 0, "需要正数参数"),
        'abs': (abs, 1, lambda _: True, "")
    }
    
    OPERATORS = {
        '+': lambda a, b: a + b,
        '-': lambda a, b: a - b,
        '*': lambda a, b: a * b,
        '/': lambda a, b: a / b if b != 0 else exec('raise ValueError("除数不能为零")'),
        '^': lambda a, b: a ** b,
        '%': lambda a, b: a % b if b != 0 else exec('raise ValueError("取模运算的除数不能为零")')
    }
    
    @handle_errors
    def calculate(self, num1, num2, operator):
        """执行二元运算"""
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
    
    def __init__(self):
        # 添加复数运算支持
        self.OPERATORS.update({
            '+c': lambda a, b: complex(a) + complex(b),
            '-c': lambda a, b: complex(a) - complex(b),
            '*c': lambda a, b: complex(a) * complex(b),
            '/c': lambda a, b: complex(a) / complex(b) if b != 0 else exec('raise ValueError("除数不能为零")')
        })
        
        self.FUNCTIONS.update({
            'abs_c': (abs, 1, lambda x: isinstance(x, complex), "需要复数参数"),
            'real': (lambda x: x.real, 1, lambda x: isinstance(x, complex), "需要复数参数"),
            'imag': (lambda x: x.imag, 1, lambda x: isinstance(x, complex), "需要复数参数")
        })

class CalculatorUI:
    """用户界面处理"""
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
        print(f"{Fore.GREEN}支持函数:{Style.RESET_ALL} {', '.join(CalculatorCore.FUNCTIONS.keys())}")
        print(f"{Fore.GREEN}命令:{Style.RESET_ALL}")
        print("  q - 退出  h - 帮助  c - 清屏  l - 历史  m - 多行模式")

    def get_expression(self):
        """获取用户输入（支持多行）"""
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
class ScientificCalculator:
    def __init__(self):
        self.history = HistoryManager()
        self.core = CalculatorCore()
        self.ui = CalculatorUI(self.core, self.history)

    def run(self):
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
        """处理单个表达式"""
        # 清理输入并解析
        expr = re.sub(r'\s+', ' ', expr).strip()

        # 尝试匹配函数调用
        if func_match := re.match(r"^([a-z]+)\(?([+-]?\d+\.?\d*(?:e[+-]?\d+)?)\)?$", expr, re.I):
            func_name, param = func_match.groups()
            param = float(param)
            result = self.core.process_function(func_name.lower(), param)
            return result, f"{func_name}({param}) = {result:.6g}"

        # 尝试匹配二元运算
        if bin_match := re.match(r"^([+-]?\d+\.?\d*(?:e[+-]?\d+)?)([+\-*/%^])([+-]?\d+\.?\d*(?:e[+-]?\d+)?)$", expr, re.I):
            num1_str, operator, num2_str = bin_match.groups()
            num1, num2 = float(num1_str), float(num2_str)
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
    