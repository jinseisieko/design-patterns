"""Abstract Factory Pattern Demonstration (C++).

Real-world context: Cross-platform GUI toolkit that creates families of related
widgets (buttons, text fields) for different operating systems.

Anti-pattern warning: Complex hierarchy - Adding new product types requires
modifying all concrete factories, violating Open-Closed Principle.
"""

CPP_CODE = r"""#include <iostream>
#include <memory>

// Abstract Product: Button
class Button {
public:
    virtual void render() = 0;
    virtual ~Button() = default;
};

// Abstract Product: TextField
class TextField {
public:
    virtual void addText(const std::string& text) = 0;
    virtual ~TextField() = default;
};

// Concrete Product: WindowsButton
class WindowsButton : public Button {
public:
    void render() override {
        std::cout << "Rendering a native Windows button.\n";
    }
};

// Concrete Product: WindowsTextField
class WindowsTextField : public TextField {
public:
    void addText(const std::string& text) override {
        std::cout << "Adding text '" << text << "' to a Windows text field.\n";
    }
};

// Concrete Product: MacButton
class MacButton : public Button {
public:
    void render() override {
        std::cout << "Rendering a native Mac button.\n";
    }
};

// Concrete Product: MacTextField
class MacTextField : public TextField {
public:
    void addText(const std::string& text) override {
        std::cout << "Adding text '" << text << "' to a Mac text field.\n";
    }
};

// Abstract Factory
class GUIFactory {
public:
    virtual std::unique_ptr<Button> createButton() = 0;
    virtual std::unique_ptr<TextField> createTextField() = 0;
    virtual ~GUIFactory() = default;
};

// Concrete Factory: Windows Factory
class WindowsGUIFactory : public GUIFactory {
public:
    std::unique_ptr<Button> createButton() override {
        return std::make_unique<WindowsButton>();
    }
    std::unique_ptr<TextField> createTextField() override {
        return std::make_unique<WindowsTextField>();
    }
};

// Concrete Factory: Mac Factory
class MacGUIFactory : public GUIFactory {
public:
    std::unique_ptr<Button> createButton() override {
        return std::make_unique<MacButton>();
    }
    std::unique_ptr<TextField> createTextField() override {
        return std::make_unique<MacTextField>();
    }
};

// Client Code
void clientCode(std::unique_ptr<GUIFactory> factory) {
    auto button = factory->createButton();
    auto textField = factory->createTextField();
    button->render();
    textField->addText("Hello, World!");
}

int main() {
    std::cout << "=== Windows GUI ===\n";
    clientCode(std::make_unique<WindowsGUIFactory>());
    
    std::cout << "\n=== Mac GUI ===\n";
    clientCode(std::make_unique<MacGUIFactory>());
}"""

BEFORE_CODE = r"""// Without Abstract Factory - client code creates objects directly
void createUI(bool isWindows) {
    if (isWindows) {
        WindowsButton* btn = new WindowsButton();
        WindowsTextField* txt = new WindowsTextField();
    } else {
        MacButton* btn = new MacButton();
        MacTextField* txt = new MacTextField();
    }
    // Problem: Mixed widget types possible, hard to extend
}"""

AFTER_CODE = r"""// With Abstract Factory - consistent family of objects
void createUI(std::unique_ptr<GUIFactory> factory) {
    auto btn = factory->createButton();
    auto txt = factory->createTextField();
    // Guaranteed compatible widgets
}"""


def demonstrate() -> dict:
    """Execute the Abstract Factory pattern demonstration.

    Returns:
        Dictionary containing demonstration output data.
    """
    return {
        "cpp_code": CPP_CODE,
        "before_code": BEFORE_CODE,
        "after_code": AFTER_CODE,
        "intent": (
            "Provides an interface for creating families of related or dependent "
            "objects without specifying their concrete classes."
        ),
        "context": (
            "Cross-platform GUI toolkit - creating families of related widgets "
            "(buttons, text fields) for Windows, macOS, Linux."
        ),
        "pros": [
            "Ensures compatibility between products in a family",
            "Avoids tight coupling between client and concrete classes",
            "Single responsibility: creation logic is centralized",
        ],
        "cons": [
            "Complex class hierarchy",
            "Adding new product types requires modifying all factories",
        ],
        "anti_pattern": (
            "Complex Hierarchy: Adding new product types requires modifying all "
            "concrete factories, violating Open-Closed Principle. Consider if "
            "Factory Method or simple factories would suffice."
        ),
        "uml_diagram": """
┌─────────────────────┐     ┌─────────────────────┐
│     GUIFactory      │     │       Button        │
├─────────────────────┤     ├─────────────────────┤
│ +createButton()     │────>│ +render()           │
│ +createTextField()  │     └─────────────────────┘
└─────────────────────┘              ▲
          │                          │
    ┌─────┴─────┐           ┌───────┴───────┐
    ▼           ▼           ▼               ▼
┌────────┐ ┌────────┐ ┌──────────┐  ┌──────────┐
│Windows │ │  Mac   │ │WindowsBtn│  │  MacBtn  │
│ Factory│ │ Factory│ └──────────┘  └──────────┘
└────────┘ └────────┘""",
    }
