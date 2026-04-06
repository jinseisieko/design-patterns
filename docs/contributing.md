# Contributing Guide

Thank you for your interest in contributing to the Design Patterns Demo Application!

## Setting Up Development Environment

1. Fork and clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
3. Install development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```
4. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

## Adding a New Design Pattern

### Step 1: Create the Pattern Module

Create a new Python file in the appropriate category directory:
- `patterns/creational/` for creational patterns
- `patterns/structural/` for structural patterns
- `patterns/behavioral/` for behavioral patterns

### Step 2: Implement the demonstrate() Function

Every pattern module must expose a `demonstrate()` function:

```python
def demonstrate() -> dict:
    """Execute the pattern demonstration.
    
    Returns:
        Dictionary containing demonstration output and anti-pattern warning.
    """
    return {
        "key": "value",
        "anti_pattern": "Warning about pattern misuse",
    }
```

### Step 3: Register the Pattern

Add your pattern to `patterns/__init__.py`:

```python
from patterns.creational.your_pattern import demonstrate as your_pattern_demo

_pattern_registry["creational/your_pattern"] = {
    "category": "Creational",
    "name": "Your Pattern",
    "description": "Brief description",
    "demo_func": your_pattern_demo,
}
```

### Step 4: Write Tests

Create tests in `tests/test_patterns/test_your_pattern.py`.

### Step 5: Document the Pattern

Create a Markdown file in `docs/patterns/<category>/your_pattern.md`.

## Code Style

We use:
- **Ruff** for linting
- **Black** for formatting

These run automatically via pre-commit hooks.

## Submitting Changes

1. Create a feature branch: `git checkout -b feature/pattern-name`
2. Make your changes
3. Run tests: `pytest`
4. Commit with a descriptive message
5. Push and submit a Pull Request

See [CONTRIBUTING.md](../CONTRIBUTING.md) for full details.
