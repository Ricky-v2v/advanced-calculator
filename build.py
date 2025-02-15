import PyInstaller.__main__
import os
import shutil
import platform
import yaml
import sys

def build():
    try:
        # 清理旧的构建文件
        if os.path.exists('dist'):
            shutil.rmtree('dist')
        if os.path.exists('build'):
            shutil.rmtree('build')
        
        # 基本配置
        common_options = [
            '--onefile',
            '--clean',
            '--add-data', f'config.yaml{os.pathsep}.',
            '--add-data', f'i18n/*{os.pathsep}i18n',
            '--add-data', f'utils/*{os.pathsep}utils',  # 添加这行
        ]
        
        # 获取版本号
        with open('config.yaml', 'r') as f:
            version = yaml.safe_load(f)['version']
        
        print(f"开始构建版本 {version}...")
        
        # 构建 CLI 版本
        print("构建命令行版本...")
        PyInstaller.__main__.run([
            'calculator_cli.py',
            f'--name=calculator-cli-{platform.system().lower()}',
            *common_options,
        ])
        
        # 构建 GUI 版本
        print("构建图形界面版本...")
        PyInstaller.__main__.run([
            'gui_calculator.py',
            f'--name=calculator-gui-{platform.system().lower()}',
            '--windowed',
            *common_options,
        ])
        
        print("构建完成！")
        return True
        
    except Exception as e:
        print(f"构建失败: {str(e)}")
        return False

if __name__ == "__main__":
    success = build()
    sys.exit(0 if success else 1)