# 计算器开发者指南

## 项目结构
- calculator_cli.py: 命令行界面实现
- gui_calculator.py: 图形界面实现
- unit_converter.py: 单位转换功能
- utils/: 工具函数
  - logger.py: 日志处理
  - version_checker.py: 版本检查

## 核心组件
### CalculatorCore
- 负责所有计算逻辑
- 支持基本运算、科学函数和复数运算
- 使用装饰器进行错误处理

### HistoryManager
- 管理计算历史记录
- 支持持久化存储
- 提供搜索功能

### CalculatorUI
- 处理用户输入输出
- 支持命令自动补全
- 提供多行输入模式

## 扩展指南
### 添加新运算符
1. 在 `CalculatorCore.OPERATORS` 中添加新运算符
2. 定义运算逻辑和错误处理

### 添加新函数
1. 在 `CalculatorCore.FUNCTIONS` 中添加新函数
2. 指定参数个数和验证规则

### 添加新特性
1. 遵循现有错误处理机制
2. 更新帮助文档
3. 添加相应的测试用例