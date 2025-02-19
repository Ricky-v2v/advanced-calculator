import sys
import os
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QTabWidget, QPushButton, QLineEdit, QLabel, QGridLayout,
    QComboBox, QMessageBox, QListWidget, QHBoxLayout
)
from PyQt6.QtCore import Qt
from src.calculator_cli import ScientificCalculator
from src.unit_converter import UnitConverter, UnitType
from src.i18n.translator import Translator
# 添加 HistoryManager 的导入
from src.history_manager import HistoryManager

class CalculatorGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.translator = Translator()
        self.calculator = ScientificCalculator()
        # 确保 calculator 和 translator 正确初始化
        self.calculator.translator = self.translator
        self.calculator.history = HistoryManager()  # 显式初始化历史记录管理器
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle(self.translator.translate("calculator_title"))
        self.setGeometry(100, 100, 600, 400)
        self.setMinimumSize(400, 500)
        
        # 创建中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # 创建标签页
        tabs = QTabWidget()
        layout.addWidget(tabs)
        
        # 添加各个标签页
        basic_tab = QWidget()
        unit_tab = QWidget()
        history_tab = QWidget()
        
        # 修改标签页文本
        tabs.addTab(basic_tab, self.translator.translate("basic_calc"))
        tabs.addTab(unit_tab, self.translator.translate("unit_converter"))
        tabs.addTab(history_tab, self.translator.translate("history"))
        
        self.setup_basic_calc(basic_tab)
        self.setup_unit_converter(unit_tab)
        self.setup_history(history_tab)

    def setup_basic_calc(self, parent):
        layout = QVBoxLayout(parent)
        layout.setSpacing(5)
        
        # 输入框样式优化
        self.expr_input = QLineEdit()
        self.expr_input.setPlaceholderText(self.translator.translate("enter_expression"))
        self.expr_input.setMinimumHeight(30)
        self.expr_input.returnPressed.connect(self.calculate)
        layout.addWidget(self.expr_input)
        
        # 按钮网格
        button_grid = QGridLayout()
        
        # 添加清除按钮
        clear_btn = QPushButton("C")
        clear_btn.clicked.connect(self.clear_input)
        button_grid.addWidget(clear_btn, 0, 0)
        
        basic_buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', '=', '+'
        ]
        
        # 修复按钮点击事件处理
        for i, row in enumerate([basic_buttons[i:i+4] for i in range(0, len(basic_buttons), 4)]):
            for j, text in enumerate(row):
                button = QPushButton(text)
                if text == '=':
                    button.clicked.connect(self.calculate)
                else:
                    button.clicked.connect(lambda checked, t=text: self.append_text(t))
                button_grid.addWidget(button, i+1, j)
        
        # 科学函数按钮布局
        science_buttons = [
            ('sin', 'cos', 'tan', 'log'),
            ('sqrt', 'abs', '(', ')')
        ]
        science_grid = QGridLayout()
        for i, row in enumerate(science_buttons):
            for j, text in enumerate(row):
                button = QPushButton(text)
                button.clicked.connect(lambda checked, t=text: self.append_text(t + '(' if t not in ['(', ')'] else t))
                science_grid.addWidget(button, i, j)
        
        layout.addLayout(button_grid)
        layout.addLayout(science_grid)
        
        # 设置按钮统一样式
        for button in parent.findChildren(QPushButton):
            button.setMinimumSize(40, 40)
            button.setStyleSheet("""
                QPushButton {
                    background-color: #f0f0f0;
                    border: 1px solid #ccc;
                    border-radius: 2px;
                }
                QPushButton:hover {
                    background-color: #e0e0e0;
                }
                QPushButton:pressed {
                    background-color: #d0d0d0;
                }
            """)

    # 添加新方法
    def append_text(self, text):
        """向输入框添加文本"""
        current_text = self.expr_input.text()
        self.expr_input.setText(current_text + text)

    def setup_unit_converter(self, parent):
        layout = QVBoxLayout(parent)
        grid = QGridLayout()
        
        # 单位类型选择
        grid.addWidget(QLabel(self.translator.translate("unit_type")), 0, 0)
        self.unit_type_combo = QComboBox()
        self.unit_type_combo.addItems([t.value for t in UnitType])
        self.unit_type_combo.currentTextChanged.connect(self.update_unit_options)
        grid.addWidget(self.unit_type_combo, 0, 1)
        
        # 输入值
        grid.addWidget(QLabel(self.translator.translate("value")), 1, 0)
        self.value_input = QLineEdit()
        grid.addWidget(self.value_input, 1, 1)
        
        # 单位选择
        grid.addWidget(QLabel(self.translator.translate("from")), 2, 0)
        self.from_unit_combo = QComboBox()
        grid.addWidget(self.from_unit_combo, 2, 1)
        
        grid.addWidget(QLabel(self.translator.translate("to")), 3, 0)
        self.to_unit_combo = QComboBox()
        grid.addWidget(self.to_unit_combo, 3, 1)
        
        # 转换按钮
        convert_btn = QPushButton(self.translator.translate("convert"))
        convert_btn.clicked.connect(self.convert_units)
        grid.addWidget(convert_btn, 4, 0, 1, 2)  # 跨两列
        
        # 结果显示
        self.result_label = QLabel()
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        grid.addWidget(self.result_label, 5, 0, 1, 2)  # 跨两列
        
        layout.addLayout(grid)
        layout.addStretch()  # 添加弹性空间
        
        # 初始化单位选项
        self.update_unit_options()

    # 添加新方法
    def clear_input(self):
        """清除输入框内容"""
        self.expr_input.clear()

    def keyPressEvent(self, event):
        """处理键盘事件"""
        if event.key() == Qt.Key.Key_Escape:
            self.clear_input()
        else:
            super().keyPressEvent(event)

    def setup_history(self, parent):
        layout = QVBoxLayout(parent)
        layout.setSpacing(5)
        
        # 搜索框优化
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(self.translator.translate("search_history"))
        self.search_input.textChanged.connect(self.filter_history)
        search_layout.addWidget(self.search_input)
        
        # 历史列表优化
        self.history_list = QListWidget()
        self.history_list.setAlternatingRowColors(True)  # 交替行颜色
        self.history_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #ccc;
                border-radius: 2px;
            }
            QListWidget::item {
                padding: 5px;
            }
        """)
        
        layout.addLayout(search_layout)
        layout.addWidget(self.history_list)
        self.update_history_list()

    def calculate(self):
        try:
            expr = self.expr_input.text()
            result, record = self.calculator.process_expression(expr)
            self.calculator.history.add_record(record)
            self.expr_input.setText(str(result))
            self.update_history_list()
        except Exception as e:
            QMessageBox.critical(self, 
                               self.translator.translate("error"),
                               self.translator.translate("calc_error").format(str(e)))

    def convert_units(self):
        try:
            if not self.value_input.text():
                raise ValueError(self.translator.translate("error.value_required"))
                
            value = float(self.value_input.text())
            result = UnitConverter.convert(
                value,
                self.from_unit_combo.currentText(),
                self.to_unit_combo.currentText()
            )
            # 先更新显示结果
            self.result_label.setText(
                f"{value} {self.from_unit_combo.currentText()} = "
                f"{result:.6g} {self.to_unit_combo.currentText()}"
            )
            
            # 添加历史记录
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            record = f"[{timestamp}] " + self.translator.translate("unit_conversion_record").format(
                value,
                self.from_unit_combo.currentText(),
                f"{result:.6g}",
                self.to_unit_combo.currentText()
            )
            
            # 确保历史记录被正确添加
            if hasattr(self.calculator, 'history'):
                self.calculator.history.add_record(record)
                self.update_history_list()  # 立即更新显示
        except ValueError as e:
            QMessageBox.critical(self, 
                           self.translator.translate("error.title"),
                           str(e))
        except Exception as e:
            QMessageBox.critical(self, 
                           self.translator.translate("error.title"),
                           self.translator.translate("error.convert_error").format(str(e)))

    def update_unit_options(self):
        unit_type = UnitType(self.unit_type_combo.currentText())
        units = list(UnitConverter.CONVERSIONS[unit_type].keys())
        self.from_unit_combo.clear()
        self.to_unit_combo.clear()
        self.from_unit_combo.addItems(units)
        self.to_unit_combo.addItems(units)

    def filter_history(self):
        search_term = self.search_input.text().lower()
        self.update_history_list(search_term)

    def update_history_list(self, search_term=''):
        self.history_list.clear()
        if hasattr(self.calculator, 'history'):
            history_items = self.calculator.history.get_recent_history()
            for item in history_items:
                if search_term.lower() in item.lower():
                    self.history_list.addItem(item)
            # 滚动到最新记录
            if self.history_list.count() > 0:
                self.history_list.scrollToBottom()

def main():
    os.environ['LANG'] = 'en_US.UTF-8'
    os.environ['LC_ALL'] = 'en_US.UTF-8'
    
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    calculator = CalculatorGUI()
    calculator.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()