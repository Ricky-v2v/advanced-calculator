# 高级科学计算器

[English](README_EN.md) | 简体中文

一个功能强大的科学计算器，支持命令行和图形界面，提供基本运算、科学函数计算、复数运算等功能。

## 功能特点

- 基本运算：+, -, *, /, ^, %
- 科学函数：sqrt, sin, cos, tan, log, log10, abs
- 复数运算：+c, -c, *c, /c, abs_c, real, imag
- 历史记录管理
- 多行输入支持
- 命令自动补全
- 国际化支持
- 自动更新检查

## 安装说明

1. 克隆仓库：
```bash
git clone https://github.com/ricky-v2v/advanced-calculator.git
cd advanced-calculator


2. 安装依赖：
```bash
pip install -r requirements.txt
 ```


## 构建可执行文件
使用 PyInstaller 构建独立可执行文件：

```bash
python build.py
 ```

## 项目结构
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

## 开发说明
- Python 版本要求：3.8+
- 使用 PyInstaller 打包
- 遵循 PEP 8 编码规范
- 使用 pytest 进行单元测试
## 许可证
MIT License