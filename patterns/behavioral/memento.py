"""Memento Pattern Demonstration (C++).

Real-world context: Text editor save/restore - capturing and externalizing an
object's internal state without violating encapsulation.

Anti-pattern warning: Large state snapshots - Saving entire object state when
only incremental changes are needed, wasting memory.
"""

CPP_CODE = r"""#include <iostream>
#include <string>
#include <memory>
#include <vector>

// Memento (opaque to caretaker)
class Memento {
private:
    std::string state;
    friend class TextEditor; // Only Editor can access
    
    explicit Memento(const std::string& s) : state(s) {}
    std::string getState() const { return state; }
};

// Originator
class TextEditor {
private:
    std::string content;
public:
    void setContent(const std::string& text) {
        content = text;
        std::cout << "Content: '" << content << "'\n";
    }
    
    std::string getContent() const { return content; }
    
    std::unique_ptr<Memento> save() {
        return std::make_unique<Memento>(content);
    }
    
    void restore(const Memento& memento) {
        content = memento.getState();
        std::cout << "Restored to: '" << content << "'\n";
    }
};

// Caretaker
class History {
private:
    std::vector<std::unique_ptr<Memento>> states;
    int index = -1;
public:
    void push(std::unique_ptr<Memento> m) {
        states.resize(index + 1);
        states.push_back(std::move(m));
        index++;
    }
    
    std::unique_ptr<Memento> pop() {
        if (index >= 0) {
            return std::make_unique<Memento>(states[index]->getState());
            index--;
        }
        return nullptr;
    }
    
    bool canUndo() const { return index >= 0; }
};

int main() {
    TextEditor editor;
    History history;
    
    editor.setContent("Version 1");
    history.push(editor.save());
    
    editor.setContent("Version 2");
    history.push(editor.save());
    
    editor.setContent("Version 3");
    
    std::cout << "Current: " << editor.getContent() << "\n";
    
    history.pop();
    editor.restore(*history.pop());
}"""

BEFORE_CODE = r"""// Without Memento - exposing internal state
class TextEditor {
public:
    string content;  // Public: breaks encapsulation
};

// Client saves state directly
string savedState = editor.content;
editor.content = savedState;  // Can modify arbitrarily"""

AFTER_CODE = r"""// With Memento - encapsulated state
auto memento = editor.save();  // Opaque snapshot
editor.restore(*memento);      // Restored safely"""


def demonstrate() -> dict:
    """Execute the Memento pattern demonstration."""
    return {
        "cpp_code": CPP_CODE,
        "before_code": BEFORE_CODE,
        "after_code": AFTER_CODE,
        "intent": (
            "Captures and externalizes an object's internal state without "
            "violating encapsulation, so the object can be restored later."
        ),
        "context": (
            "Text editor undo/save - capturing snapshots of document state "
            "for undo operations."
        ),
        "pros": [
            "Preserves encapsulation boundaries",
            "Simplifies originator code",
            "Easy to add versioning/history",
        ],
        "cons": [
            "Memory intensive for large state snapshots",
            "Caretaker may incur deletion costs tracking mementos",
        ],
        "anti_pattern": (
            "Large State Snapshots: Don't save entire object state when only "
            "incremental changes matter. Consider delta-based snapshots for "
            "memory efficiency."
        ),
        "uml_diagram": """
┌─────────────────────┐     ┌──────────────────┐
│    TextEditor       │     │    Memento       │
│   (Originator)      │────>│ (opaque object)  │
├─────────────────────┤     ├──────────────────┤
│ -content            │     │ -state           │
├─────────────────────┤     └──────────────────┘
│ +save() -> Memento  │              │
│ +restore(Memento)   │              │
│ +setContent()       │              │
└─────────────────────┘              │
                                     ▼
                          ┌──────────────────┐
                          │    History       │
                          │   (Caretaker)    │
                          ├──────────────────┤
                          │ -states[]        │
                          │ +push(Memento)   │
                          │ +pop() -> Memento│
                          └──────────────────┘""",
    }
