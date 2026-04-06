# Design Patterns Documentation

Welcome to the comprehensive documentation for the Design Patterns Demo Application.

## Overview

This application demonstrates all 23 Gang of Four design patterns through realistic C++ implementations, served via a Python/Flask web application. Each pattern is demonstrated in a tangible scenario—game engines, networking, UI frameworks—bridging the gap between theoretical knowledge and practical application.

## Getting Started

### Prerequisites

- Python 3.10+
- pip
- Virtual environment support

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd design-patterns

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements-dev.txt

# Run the application
flask --app app run --debug
```

### Running Tests

```bash
pytest --cov=patterns --cov=app
```

## Pattern Categories

Design patterns are categorized into three main types:

### Creational Patterns
Deal with object creation mechanisms, trying to create objects in a manner suitable to the situation.

### Structural Patterns
Deal with object composition, trying to ease the design by identifying a simple way to realize relationships between entities.

### Behavioral Patterns
Deal with object communication, trying to identify common communication patterns between objects.

## Architecture

The application uses:
- **Flask** with the Application Factory pattern
- **Blueprints** for modular routing
- **Pattern Registry** for decoupled pattern registration
- **Jinja2** for server-side rendering

See the [Contributing Guide](contributing.md) for details on adding new patterns.
