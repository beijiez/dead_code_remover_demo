# Dead Code Remover Demo

This project provides a tool to analyze and remove unused functions and imports from Python files. It helps keep your codebase clean and maintainable.

## Features

- Detects unused functions and imports in Python files.
- Removes unused code while preserving the functionality of the remaining code.
- Outputs a cleaned version of the file or overwrites the original file.

## Installation

1. Clone this repository.
2. Install the required dependencies using pip:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

To analyze and clean a Python file, run the following command:

```bash
python -m cleaner.cli --file examples/sample.py
```

### Options

- `--file`: Path to the Python file to be analyzed and cleaned.
- `--overwrite`: If specified, the original file will be overwritten with the cleaned version. Otherwise, a new file with `_cleaned` appended to the name will be created.
- `--explain-only`: Only explain unused code without removing it.
- `--patch`: Generate a `.patch` file instead of saving the cleaned file.
- `--interactive`: Prompt before deleting each unused function or import.
- `--explain`: Use AI to explain why code is considered dead.

### Example

Given the file `examples/sample.py`:

```python
import os
import sys

def unused_function():
    print("I am never called!")

def used_function(x):
    return x * 2

def plus_one(x):
    return x + 1

result = used_function(5)
```

Running the command:

Produces explanations for unused functions and imports, will call an AI client. The current model is `EleutherAI/gpt-neo-1.3B`. 

```bash
python -m cleaner.cli --file examples/sample.py --explain
```

To clean the file interactively:

```bash
python -m cleaner.cli --file examples/sample.py --interactive
```

To generate a patch file:

```bash
python -m cleaner.cli --file examples/sample.py --patch
```

To overwrite the original file instead:

```bash
python -m cleaner.cli --file examples/sample.py --overwrite
```

The flags can be combined as well. For example:

```bash
python -m cleaner.cli --file examples/sample.py --overwrite --explain-only
```

## License

This project is licensed under the MIT License.