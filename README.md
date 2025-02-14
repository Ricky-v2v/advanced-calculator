# 高级科学计算器

一个功能强大的科学计算器，支持基本运算、科学函数、单位转换、复数运算等功能。

## 功能特点

- 基本数学运算
- 科学函数计算（sin, cos, log等）
- 单位转换（长度、重量、温度、面积）
- 复数运算
- 历史记录管理
- 命令行和图形界面两种使用方式

## 安装方法

### 方法一：使用可执行文件

直接下载并运行对应系统的可执行文件：
- calculator-cli：命令行版本
- calculator-gui：图形界面版本

### 方法二：从源码安装

```bash
# 创建并激活虚拟环境
python -m venv venv
source venv/bin/activate  # Windows 使用: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 安装项目
pip install .

## 系统要求
- Python 3.8 或更高版本
- 操作系统：Windows/macOS/Linux
# 运行计算器
calc-cli  # 命令行版本
calc-gui  # 图形界面版本