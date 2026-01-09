# Repository Guidelines

## Coding Style Requirements

- I need code to be as short as possible, no error handling is needed.
- This is research code, so it **doesn't** need to be written with engineering practices, such as:
  - Error handling: Ensure you know the variables and that they are written correctly, all robustness branches should be deleted. If they are correct, additional error checks are unnecessary.  
  - Defensive programming: Understand the variables in advance. For example, instead of using `if dim == 3` or `assert dim == 3` to verify input dimensions, ensure the input is 3D and write the code to handle it appropriately.  
  - Unnecessary helper functions, do not write helper function that is only used once or twice, like `_prepare_*`, and keep function arguments as minimal as possible.
  - Compatibility with previous interfaces
  - Other engineering practices like real world production environment code

## Coding Details Requirements

- When you write code:
  - Code must be in English.
  - Comments must be in English.
  - For every function/method, include detailed docstrings that explain purpose, parameters (type AND shape/dimensions), and return values (type AND shape).

```python
"""Visualize a normalized joint trajectory for the specified hand.

Parameters
----------
hand_name : str
    Logical identifier for the target hand, e.g. ``"xhand_right"``.
joint_series : np.ndarray, shape=(T, M), dtype=float32
    Normalized joint commands with values expected in ``[-1.0, 1.0]``.
"""
```

- Other code explanation outside coding files should be in Simplified Chinese.
- Files and folders should be named in lowercase letters with underscores (e.g., `my_module.py`) .
- Use snake_case (lowercase letters and underscores) for function and variable names, and PascalCase (CapWords or CamelCase) for class names.

## Python Environment Requirements (**If it's a new project or a project already using uv, ignore this in IsaacLab style repo**)

- Python code should be managed using `uv` .
- All files should be run using `uv run -m Folder.filename` or `uv run -m Folder.filename` to execute, instead of `uv run Folder/filename.py` to ensure the correct module path is used for imports.
- Module import in the same project should use absolute imports (e.g., `from AnotherFolder.utils import helper_function`) instead of relative imports (e.g., `from .utils import helper_function`) to avoid issues with module paths when running the code.