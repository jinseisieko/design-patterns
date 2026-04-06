"""Mediator Pattern Demonstration (C++).

Real-world context: GUI dialog box - encapsulating how UI controls interact so
they don't refer to each other explicitly.

Anti-pattern warning: God Object mediator - Creating a mediator that knows about
too many controls, becoming a complex dependency hub.
"""

CPP_CODE = r"""#include <iostream>
#include <memory>
#include <string>

// Forward declaration
class UIMediator;

// Colleague Base
class UIControl {
protected:
    std::shared_ptr<UIMediator> mediator;
    std::string name;
public:
    UIControl(const std::string& n) : name(n) {}
    virtual ~UIControl() = default;
    void setMediator(std::shared_ptr<UIMediator> m) { mediator = m; }
    virtual void onChange() = 0;
    const std::string& getName() const { return name; }
};

// Concrete Colleagues
class TextBox : public UIControl {
private:
    std::string text;
public:
    TextBox() : UIControl("UsernameBox") {}
    void setText(const std::string& t) { text = t; onChange(); }
    bool isEmpty() const { return text.empty(); }
    void onChange() override {
        if (mediator) mediator->valueChanged(this);
    }
};

class Button : public UIControl {
private:
    bool enabled = false;
public:
    Button() : UIControl("SubmitButton") {}
    void setEnabled(bool e) { enabled = e; }
    bool isEnabled() const { return enabled; }
    void onChange() override {}
};

class ListBox : public UIControl {
private:
    std::vector<std::string> items;
public:
    ListBox() : UIControl("SuggestionsList") {}
    void clear() { items.clear(); }
    void addItem(const std::string& item) { items.push_back(item); }
    void onChange() override {
        if (mediator) mediator->listChanged(this);
    }
};

// Mediator
class UIMediator {
private:
    std::shared_ptr<TextBox> textBox;
    std::shared_ptr<Button> button;
    std::shared_ptr<ListBox> listBox;
public:
    UIMediator(std::shared_ptr<TextBox> t, std::shared_ptr<Button> b, 
               std::shared_ptr<ListBox> l)
        : textBox(std::move(t)), button(std::move(b)), listBox(std::move(l)) {}
    
    void valueChanged(UIControl* control) {
        if (control == textBox.get()) {
            button->setEnabled(!textBox->isEmpty());
            listBox->clear();
            if (!textBox->isEmpty()) {
                listBox->addItem("suggestion1");
                listBox->addItem("suggestion2");
            }
        }
    }
    
    void listChanged(UIControl* control) {
        std::cout << "List changed, updating UI...\n";
    }
};

int main() {
    auto textBox = std::make_shared<TextBox>();
    auto button = std::make_shared<Button>();
    auto listBox = std::make_shared<ListBox>();
    
    auto mediator = std::make_shared<UIMediator>(textBox, button, listBox);
    textBox->setMediator(mediator);
    button->setMediator(mediator);
    listBox->setMediator(mediator);
    
    std::cout << "Button enabled? " << (button->isEnabled() ? "Yes" : "No") << "\n";
    
    textBox->setText("user123");
    std::cout << "Button enabled? " << (button->isEnabled() ? "Yes" : "No") << "\n";
}"""

BEFORE_CODE = r"""// Without Mediator - controls know about each other
class TextBox {
    Button* submitButton;
    ListBox* suggestions;
    
    void onChange() {
        submitButton->setEnabled(!text.empty());
        suggestions->clear();
        suggestions->add(getSuggestions());
    }
};
// Tight coupling, hard to reuse controls"""

AFTER_CODE = r"""// With Mediator - controls communicate through mediator
class TextBox {
    void onChange() {
        mediator->valueChanged(this);
    }
};
// Controls are decoupled and reusable"""


def demonstrate() -> dict:
    """Execute the Mediator pattern demonstration."""
    return {
        "cpp_code": CPP_CODE,
        "before_code": BEFORE_CODE,
        "after_code": AFTER_CODE,
        "intent": (
            "Defines an object that encapsulates how a set of objects interact. "
            "Promotes loose coupling by preventing objects from referring to each other."
        ),
        "context": (
            "GUI dialog box - text field, button, and list box communicate "
            "through a mediator instead of directly."
        ),
        "pros": [
            "Decouples colleagues from each other",
            "Centralizes interaction logic",
            "Makes colleagues reusable",
        ],
        "cons": [
            "Mediator can become a God Object",
            "Adds another layer of indirection",
        ],
        "anti_pattern": (
            "God Object Mediator: Don't create a mediator that coordinates too "
            "many unrelated controls. Split into multiple focused mediators if "
            "the interaction logic becomes complex."
        ),
        "uml_diagram": """
┌─────────────────┐         ┌─────────────────┐
│  UIMediator     │<───────>│  UIControl      │
├─────────────────┤         ├─────────────────┤
│ -textBox        │         │ -mediator       │
│ -button         │         │ +onChange()     │
│ -listBox        │         └─────────────────┘
├─────────────────┤                  ▲
│ +valueChanged() │            ┌─────┼──────┐
│ +listChanged()  │            ▼     ▼      ▼
└─────────────────┘        ┌────┐ ┌────┐ ┌────┐
                           │Txt │ │Btn │ │List│
                           └────┘ └────┘ └────┘""",
    }
