# Advanced Scientific Calculator

[简体中文](README.md) | English

A powerful scientific calculator with both command-line and graphical interfaces, supporting basic arithmetic, scientific functions, and complex number operations.

## Key Features

- Basic Operations: +, -, *, /, ^, %
- Scientific Functions: sqrt, sin, cos, tan, log, log10, abs
- Complex Number Operations: +c, -c, *c, /c, abs_c, real, imag
- History Management
- Multi-line Input Support
- Command Auto-completion
- Internationalization Support
- Automatic Update Check

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ricky-v2v/advanced-calculator.git
cd advanced-calculator

2. Install dependencies:
```bash
pip install -r requirements.txt
 ```

## Usage

## Building Executable
Build standalone executable using PyInstaller:

```bash
python build.py
 ```

## Project Structure
```plaintext
advanced-calculator/
├── src/
│   ├── calculator_cli.py    # 命令行界面主程序
│   ├── gui_calculator.py    # 图形界面主程序
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── logger.py       # 日志工具
│   │   └── version_checker.py  # 版本检查
│   └── i18n/
│       ├── __init__.py
│       └── zh_CN.json      # 中文翻译
├── tests/
│   └── unit/
│       ├── __init__.py
│       ├── test_calculator_core.py
│       ├── test_calculator_ui.py
│       ├── test_history_manager.py
│       └── test_scientific_calculator.py
├── config.yaml             # 配置文件
├── build.py               # 构建脚本
├── requirements.txt       # 项目依赖
├── README.md             # 中文文档
├── README_EN.md          # 英文文档
└── calc_history.json     # 历史记录文件
 ```

## Development Notes
- Python Version: 3.8+
- Packaging: PyInstaller
- Coding Style: PEP 8
- Testing: pytest
## License
MIT License