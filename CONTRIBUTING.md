# Contributing to Design Patterns Demo

Thank you for your interest in contributing to this educational project! This document provides guidelines and instructions for contributing.

## 🎯 Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md).

## 🚀 Getting Started

### Development Environment Setup

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

### Running the Application

```bash
flask --app app run --debug
```

### Running Tests

```bash
pytest --cov=patterns --cov=app
```

## 📝 Adding a New Design Pattern

We welcome contributions that add new design patterns to the application. Follow these steps:

### 1. Create the Pattern Module

Create a new Python file in the appropriate category directory:
- `patterns/creational/` for creational patterns
- `patterns/structural/` for structural patterns
- `patterns/behavioral/` for behavioral patterns

### 2. Implement the `demonstrate()` Function

Every pattern module must expose a `demonstrate()` function that returns a dictionary with demonstration data:

```python
def demonstrate() -> dict:
    """Execute the pattern demonstration.
    
    Returns:
        Dictionary containing:
        - output data for the template
        - anti_pattern warning message
    """
    return {
        "key": "value",
        "anti_pattern": "Warning message about misuse",
    }
```

### 3. Register the Pattern

Add your pattern to the registry in `patterns/__init__.py`:

```python
from patterns.creational.your_pattern import demonstrate as your_pattern_demo

_pattern_registry = {
    # ... existing patterns
    "creational/your_pattern": {
        "category": "Creational",
        "name": "Your Pattern",
        "description": "Brief description",
        "demo_func": your_pattern_demo,
    },
}
```

### 4. Write Tests

Create tests in `tests/test_patterns/test_your_pattern.py`:

```python
from patterns.creational.your_pattern import demonstrate


def test_demonstrate_returns_dict():
    output = demonstrate()
    assert isinstance(output, dict)


def test_demonstrate_has_anti_pattern_warning():
    output = demonstrate()
    assert "anti_pattern" in output
```

### 5. Update Templates

If needed, add rendering logic for your pattern's output in `templates/pattern_detail.html`.

### 6. Document the Pattern

Create a Markdown file in `docs/patterns/<category>/your_pattern.md` with:
- Pattern intent
- UML diagram (text-based)
- Before/After code comparison
- Pros and cons
- Real-world use cases

## 🔧 Code Style

We use automated tools to maintain code quality:

- **Ruff**: Static analysis for errors and style violations
- **Black**: Opinionated code formatter

These run automatically via pre-commit hooks. Ensure they pass before submitting PRs.

## 📤 Submitting Changes

1. Create a feature branch: `git checkout -b feature/pattern-name`
2. Make your changes
3. Run tests: `pytest`
4. Commit with a descriptive message following [Conventional Commits](https://www.conventionalcommits.org/)
5. Push to your fork and submit a Pull Request

### Pull Request Template

Please fill out the PR template provided in `.github/PULL_REQUEST_TEMPLATE.md`.

## ❓ Questions?

Feel free to open an issue for any questions or clarifications about contributing.

Thank you for contributing! 🎉
