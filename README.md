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
git clone <repository-url>
cd Calculator


2. 安装依赖：
```bash
pip install -r requirements.txt
 ```

## 使用方法
### 命令行界面
运行命令行版本：

```bash
python calculator_cli.py
 ```

支持的命令：

- q: 退出程序
- h: 显示帮助
- c: 清屏
- l: 显示历史
- m: 切换多行模式
### 图形界面
运行图形界面版本：

```bash
python gui_calculator.py
 ```

## 构建可执行文件
使用 PyInstaller 构建独立可执行文件：

```bash
python build.py
 ```

## 项目结构
```plaintext
Calculator/
├── calculator_cli.py    # 命令行界面主程序
├── gui_calculator.py    # 图形界面主程序
├── build.py            # 构建脚本
├── config.yaml         # 配置文件
├── i18n/              # 国际化文件
│   └── zh_CN.json     # 中文翻译
└── utils/             # 工具模块
    ├── logger.py      # 日志工具
    └── version_checker.py  # 版本检查
 ```

## 开发说明
- Python 版本要求：3.8+
- 使用 PyInstaller 打包
- 遵循 PEP 8 编码规范
- 使用 pytest 进行单元测试
## 许可证
MIT License