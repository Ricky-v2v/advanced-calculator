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
            'calc-cli=calculator_cli:ScientificCalculator().run',
            'calc-gui=gui_calculator:CalculatorGUI().run',
        ],
    },
)