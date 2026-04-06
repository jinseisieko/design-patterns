# C++ Design Patterns Demo - 23 Essential Patterns

An educational, open-source web application that teaches all 23 essential C++ design patterns through realistic implementations in game engines, networking, and UI frameworks.

## 🎯 Project Vision

This application teaches software design patterns through practical C++ examples grounded in real-world contexts such as game development, high-performance networking, and UI frameworks. It covers all **23 GoF design patterns** organized into three categories.

## 📐 All 23 Design Patterns

### Creational Patterns (5)
Patterns concerned with object creation mechanisms:

| Pattern | Description | Real-World Context |
|---------|-------------|-------------------|
| **Abstract Factory** | Creates families of related objects without specifying concrete classes | Cross-platform GUI toolkit |
| **Singleton** | Ensures only one instance with global access | Logger, configuration manager |
| **Factory Method** | Delegates object creation to subclasses via factory method | Payment processing gateway |
| **Builder** | Separates complex object construction from representation | HTTP request construction |
| **Prototype** | Creates objects by cloning pre-configured instances | Game enemy unit spawning |

### Structural Patterns (7)
Patterns focused on composing classes/objects into larger structures:

| Pattern | Description | Real-World Context |
|---------|-------------|-------------------|
| **Adapter** | Converts one interface to another expected by clients | Media player format support |
| **Bridge** | Decouples abstraction from implementation | Shape rendering (OpenGL/DirectX) |
| **Composite** | Composes objects into tree structures for part-whole hierarchies | Scene graphs |
| **Decorator** | Dynamically adds responsibilities without subclassing | Data encryption/compression |
| **Facade** | Simplifies interface to complex subsystem | Database manager |
| **Flyweight** | Shares data to minimize memory for many similar objects | Character glyph rendering |
| **Proxy** | Provides surrogate for controlling access | Lazy-loaded images |

### Behavioral Patterns (11)
Patterns concerned with algorithms and object communication:

| Pattern | Description | Real-World Context |
|---------|-------------|-------------------|
| **Chain of Responsibility** | Passes requests along handler chain | Multi-level logging system |
| **Command** | Encapsulates requests as objects for undo/redo | Text editor operations |
| **Interpreter** | Defines grammar representation and interpreter | Math expression evaluator |
| **Iterator** | Accesses elements sequentially without exposing representation | Custom container traversal |
| **Mediator** | Encapsulates object interactions | GUI dialog coordination |
| **Strategy** | Defines interchangeable algorithm family | Sorting algorithms |
| **Visitor** | Separates algorithms from object structure | AST traversal |
| **Observer** | One-to-many dependency for state change notification | Event system |
| **State** | Alters behavior when internal state changes | E-commerce order lifecycle |
| **Memento** | Captures/externalizes state for restoration | Text editor save/undo |
| **Template Method** | Defines algorithm skeleton with deferrable steps | Game character turns |

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- pip

### Installation

```bash
git clone <repository-url>
cd design-patterns
python -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt
pre-commit install
```

### Run the Application

```bash
flask --app app run --debug
```

Visit `http://localhost:5000` in your browser.

### Running Tests

```bash
pytest --cov=patterns --cov=app
```

## 🏗️ Architecture

- **Flask** with Application Factory pattern
- **Blueprints** for modular routing
- **Pattern Registry** for decoupled pattern registration
- **Jinja2** for server-side rendering with C++ code display
- **SQLite** for zero-configuration database

## 📚 Documentation

Comprehensive documentation is available in the `docs/` directory:

```bash
cd docs
mkdocs serve
```

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on adding new patterns or improving existing ones.

## 📄 License

MIT License.
