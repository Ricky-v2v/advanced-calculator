from setuptools import setup, find_packages

setup(
    name="advanced-calculator",
    version="1.0.0",
    author="RickyZhu",
    description="高级科学计算器",
    packages=find_packages(),
    install_requires=[
        'colorama>=0.4.6',
        #'tkinter>=8.6',
    ],
    entry_points={
        'console_scripts': [
            'calc-cli=Calculator.calculator_cli:main',  # 更新这里
            'calc-gui=Calculator.gui_calculator:main',
        ],
    },
    python_requires='>=3.8',
)