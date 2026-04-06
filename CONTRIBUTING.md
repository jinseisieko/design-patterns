# Contributing to 23 Essential C++ Design Patterns

Thank you for your interest in contributing! This guide covers everything you need to know to contribute effectively.

## 🚀 Quick Start for Contributors

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/design-patterns.git
cd design-patterns

# Add the upstream remote to stay synced
git remote add upstream https://github.com/ORIGINAL_OWNER/design-patterns.git
```

### 2. Set Up Development Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
make install

# Run tests to verify setup
make test
```

### 3. Create a Branch

```bash
# Always branch from the latest main
git fetch upstream
git checkout main
git merge upstream/main

# Create your feature branch
git checkout -b feature/your-feature-name
# or
git checkout -b bugfix/issue-123-description
```

## 📐 Branch Naming Convention

| Prefix | Purpose | Example |
|--------|---------|---------|
| `feature/` | New features or patterns | `feature/add-visitor-pattern` |
| `bugfix/` | Bug fixes | `bugfix/singleton-thread-safety` |
| `docs/` | Documentation changes | `docs/update-facade-examples` |
| `refactor/` | Code refactoring | `refactor/extract-pattern-registry` |
| `test/` | Test additions or fixes | `test/add-command-pattern-tests` |
| `chore/` | Maintenance tasks | `chore/update-dependencies` |

## ✍️ Commit Message Convention

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Types:**
- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation
- `style` - Code style changes (formatting)
- `refactor` - Code refactoring
- `test` - Test changes
- `chore` - Build process or auxiliary tool changes

**Examples:**
```
feat(patterns): add Visitor pattern with AST example
fix(singleton): resolve thread-safety issue in logger
docs(readme): update installation instructions
test(observer): add unit tests for detach method
```

## 🔍 Code Style

We use automated tools. Run before committing:

```bash
make format   # Auto-format with black
make lint     # Check with ruff
make check    # Run both checks
```

Pre-commit hooks run these automatically on `git commit`.

## 🧪 Testing

```bash
make test     # Run all tests with coverage
pytest -v     # Verbose output
pytest -k singleton  # Run specific tests
```

All new pattern modules must include a `demonstrate()` function that returns a dictionary with:
- `cpp_code` - Full C++ implementation
- `before_code` - Code without the pattern
- `after_code` - Code with the pattern
- `intent` - Pattern description
- `context` - Real-world application
- `pros` / `cons` - Lists of advantages/disadvantages
- `anti_pattern` - Warning about misuse
- `uml_diagram` - Text-based class diagram

## 📝 Adding a New Pattern

### Step 1: Create the Module

```
patterns/
├── creational/
│   └── your_pattern.py    # New pattern
```

### Step 2: Implement `demonstrate()`

```python
def demonstrate() -> dict:
    """Execute the pattern demonstration."""
    return {
        "cpp_code": "Full C++ code here",
        "before_code": "Code without pattern",
        "after_code": "Code with pattern",
        "intent": "...",
        "context": "...",
        "pros": [...],
        "cons": [...],
        "anti_pattern": "...",
        "uml_diagram": "...",
    }
```

### Step 3: Register the Pattern

Edit `patterns/__init__.py`:

```python
from patterns.creational.your_pattern import demonstrate as your_pattern_demo

_pattern_registry["creational/your_pattern"] = {
    "category": "Creational",
    "name": "Your Pattern",
    "description": "...",
    "demo_func": your_pattern_demo,
}
```

### Step 4: Add Tests

```
tests/test_patterns/
└── test_your_pattern.py
```

### Step 5: Add Documentation

```
docs/patterns/creational/
└── your_pattern.md
```

## 📤 Submitting a Pull Request

1. Push your branch: `git push origin feature/your-feature-name`
2. Open a PR on GitHub
3. Fill out the PR template
4. Wait for CI checks to pass
5. Address review feedback
6. PR will be squash-merged into `main`

### PR Checklist

- [ ] Branch is up to date with `main`
- [ ] All tests pass (`make test`)
- [ ] Linting passes (`make lint`)
- [ ] Code is formatted (`make format`)
- [ ] New patterns have tests
- [ ] Documentation is updated

## 🏷️ Issue Labels

| Label | Purpose |
|-------|---------|
| 🐛 `bug` | Something isn't working |
| 💡 `enhancement` | New feature or improvement |
| 📚 `documentation` | Docs improvements |
| 🌟 `good first issue` | Good for newcomers |
| 🆘 `help wanted` | Extra attention needed |
| 🧪 `testing` | Test-related |
| 🔧 `ci-cd` | CI/CD pipeline |

## 🔒 Branch Protection

The `main` branch is protected:
- Direct pushes are blocked
- All changes require a PR
- PRs require at least 1 approval
- All CI checks must pass
- Branch must be up to date before merging
- PRs are squash-merged

## 📞 Getting Help

- Open an issue for bugs or feature requests
- Start a [Discussion](https://github.com/jinseisieko/design-patterns/discussions) for questions
- Check existing issues and PRs before creating new ones

Thank you for contributing! 🎉
