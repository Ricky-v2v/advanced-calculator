import tkinter as tk
from tkinter import ttk, messagebox
from calculator_cli import ScientificCalculator
from unit_converter import UnitConverter, UnitType

class CalculatorGUI:
    """图形界面计算器类
    
    功能：
    1. 基本计算界面（数字键盘和运算符）
    2. 科学函数计算（三角函数、对数等）
    3. 单位转换功能
    4. 历史记录管理和搜索
    
    界面组件：
        root (Tk): 主窗口
        notebook (Notebook): 标签页容器
        expr_var (StringVar): 表达式输入变量
        history_list (Listbox): 历史记录列表
        calculator (ScientificCalculator): 计算器核心实例
    """
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("高级科学计算器")
        self.calculator = ScientificCalculator()
        self.setup_ui()

    def setup_ui(self):
        # 创建标签页
        notebook = ttk.Notebook(self.root)
        notebook.pack(pady=10, expand=True)

        # 基本计算标签页
        basic_frame = ttk.Frame(notebook)
        notebook.add(basic_frame, text="基本计算")
        self.setup_basic_calc(basic_frame)

        # 单位转换标签页
        unit_frame = ttk.Frame(notebook)
        notebook.add(unit_frame, text="单位转换")
        self.setup_unit_converter(unit_frame)

        # 历史记录标签页
        history_frame = ttk.Frame(notebook)
        notebook.add(history_frame, text="历史记录")
        self.setup_history(history_frame)

    def setup_basic_calc(self, parent):
        # 输入框
        self.expr_var = tk.StringVar()
        entry = ttk.Entry(parent, textvariable=self.expr_var, width=40)
        entry.pack(pady=10)
    
        # 按钮框架
        btn_frame = ttk.Frame(parent)
        btn_frame.pack(pady=5)
    
        # 基本按钮
        basic_buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', '=', '+'
        ]
        
        # 添加科学函数按钮
        science_buttons = [
            'sin', 'cos', 'tan',
            'log', 'log10', 'sqrt',
            'abs', '(', ')', '^'
        ]
        
        # 布局基本按钮
        row = col = 0
        for btn in basic_buttons:
            cmd = lambda x=btn: self.button_click(x)
            ttk.Button(btn_frame, text=btn, command=cmd).grid(row=row, column=col, padx=2, pady=2)
            col += 1
            if col > 3:
                col = 0
                row += 1
        
        # 布局科学函数按钮
        science_frame = ttk.Frame(parent)
        science_frame.pack(pady=5)
        
        row = col = 0
        for btn in science_buttons:
            cmd = lambda x=btn: self.button_click(x + '(' if x not in ['(', ')', '^'] else x)
            ttk.Button(science_frame, text=btn, command=cmd).grid(row=row, column=col, padx=2, pady=2)
            col += 1
            if col > 4:
                col = 0
                row += 1

    def setup_unit_converter(self, parent):
        # 单位类型选择
        ttk.Label(parent, text="单位类型:").pack(pady=5)
        self.unit_type_var = tk.StringVar()
        unit_type_cb = ttk.Combobox(parent, textvariable=self.unit_type_var)
        unit_type_cb['values'] = [t.value for t in UnitType]
        unit_type_cb.pack(pady=5)
        unit_type_cb.bind('<<ComboboxSelected>>', self.update_unit_options)

        # 输入值
        ttk.Label(parent, text="值:").pack(pady=5)
        self.value_var = tk.StringVar()
        ttk.Entry(parent, textvariable=self.value_var).pack(pady=5)

        # 单位选择
        self.from_unit_var = tk.StringVar()
        self.to_unit_var = tk.StringVar()
        ttk.Label(parent, text="从:").pack(pady=5)
        self.from_unit_cb = ttk.Combobox(parent, textvariable=self.from_unit_var)
        self.from_unit_cb.pack(pady=5)
        
        ttk.Label(parent, text="到:").pack(pady=5)
        self.to_unit_cb = ttk.Combobox(parent, textvariable=self.to_unit_var)
        self.to_unit_cb.pack(pady=5)

        # 转换按钮
        ttk.Button(parent, text="转换", command=self.convert_units).pack(pady=10)

        # 结果显示
        self.result_var = tk.StringVar()
        ttk.Label(parent, textvariable=self.result_var).pack(pady=10)

    def setup_history(self, parent):
        # 搜索框
        search_frame = ttk.Frame(parent)
        search_frame.pack(fill=tk.X, pady=5)
        
        self.search_var = tk.StringVar()
        # 修改 trace 方法的调用方式
        self.search_var.trace_add('write', self.filter_history)  # 使用 trace_add 替代 trace
        ttk.Entry(search_frame, textvariable=self.search_var).pack(side=tk.LEFT, padx=5)
        ttk.Button(search_frame, text="搜索", command=self.filter_history).pack(side=tk.LEFT)

        # 历史列表
        self.history_list = tk.Listbox(parent, width=50, height=10)
        self.history_list.pack(pady=5, fill=tk.BOTH, expand=True)
        self.update_history_list()

    def button_click(self, value):
        if value == '=':
            self.calculate()
        else:
            self.expr_var.set(self.expr_var.get() + value)

    def calculate(self):
        try:
            expr = self.expr_var.get()
            result, record = self.calculator.process_expression(expr)
            self.calculator.history.add_record(record)
            self.expr_var.set(str(result))
            self.update_history_list()
        except Exception as e:
            messagebox.showerror("错误", str(e))

    def convert_units(self):
        try:
            value = float(self.value_var.get())
            result = UnitConverter.convert(
                value,
                self.from_unit_var.get(),
                self.to_unit_var.get()
            )
            self.result_var.set(f"{value} {self.from_unit_var.get()} = {result:.6g} {self.to_unit_var.get()}")
            
            # 添加到历史记录
            record = f"单位转换: {value} {self.from_unit_var.get()} -> {result:.6g} {self.to_unit_var.get()}"
            self.calculator.history.add_record(record)
            self.update_history_list()
        except Exception as e:
            messagebox.showerror("错误", str(e))

    def update_unit_options(self, event=None):
        unit_type = UnitType(self.unit_type_var.get())
        units = list(UnitConverter.CONVERSIONS[unit_type].keys())
        self.from_unit_cb['values'] = units
        self.to_unit_cb['values'] = units

    def filter_history(self, *args):
        self.update_history_list(self.search_var.get())

    def update_history_list(self, search_term=''):
        self.history_list.delete(0, tk.END)
        for item in self.calculator.history.get_recent_history():
            if search_term.lower() in item.lower():
                self.history_list.insert(tk.END, item)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    CalculatorGUI().run()