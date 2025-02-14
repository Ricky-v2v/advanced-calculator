import PyInstaller.__main__
import os
import platform

def build():
    # 获取系统信息
    system = platform.system().lower()
    
    # 基本配置
    common_options = [
        '--onefile',
        '--add-data=calc_history.json:.',
        '--clean',
    ]
    
    # CLI 版本
    PyInstaller.__main__.run([
        'calculator_cli.py',
        '--name=calculator-cli-' + system,
        *common_options,
    ])
    
    # GUI 版本
    PyInstaller.__main__.run([
        'gui_calculator.py',
        '--name=calculator-gui-' + system,
        '--windowed',  # GUI 程序不显示控制台
        *common_options,
    ])

if __name__ == "__main__":
    build()