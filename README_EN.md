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
git clone <repository-url>
cd Calculator

2. Install dependencies:
```bash
pip install -r requirements.txt
 ```

## Usage
### Command Line Interface
Run the CLI version:

```bash
python calculator_cli.py
 ```

Available commands:

- q: Quit program
- h: Show help
- c: Clear screen
- l: Show history
- m: Toggle multi-line mode
### Graphical Interface
Run the GUI version:

```bash
python gui_calculator.py
 ```

## Building Executable
Build standalone executable using PyInstaller:

```bash
python build.py
 ```

## Project Structure
```plaintext
Calculator/
├── calculator_cli.py    # Command line interface
├── gui_calculator.py    # Graphical interface
├── build.py            # Build script
├── config.yaml         # Configuration file
├── i18n/              # Internationalization
│   └── zh_CN.json     # Chinese translation
└── utils/             # Utility modules
    ├── logger.py      # Logging utility
    └── version_checker.py  # Version checker
 ```

## Development Notes
- Python Version: 3.8+
- Packaging: PyInstaller
- Coding Style: PEP 8
- Testing: pytest
## License
MIT License