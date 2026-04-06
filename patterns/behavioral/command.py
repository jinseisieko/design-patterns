"""Command Pattern Demonstration (C++).

Real-world context: Undo/Redo functionality for a text editor - each action
is wrapped in a Command object that can be executed and undone.

Anti-pattern warning: Command Explosion - Creating a separate command object
for every tiny atomic action, leading to a proliferation of small classes.
"""

CPP_CODE = r"""#include <iostream>
#include <vector>
#include <memory>
#include <string>

// Receiver
class TextEditor {
private:
    std::string content;
public:
    void insertText(const std::string& text) {
        content += text;
        std::cout << "Inserted: '" << text << "'\n";
    }
    void deleteText(size_t len) {
        if (content.length() >= len) {
            content.erase(content.length() - len);
            std::cout << "Deleted " << len << " chars\n";
        }
    }
    void print() const {
        std::cout << "Content: '" << content << "'\n";
    }
};

// Command Interface
class Command {
public:
    virtual ~Command() = default;
    virtual void execute() = 0;
    virtual void undo() = 0;
};

// Insert Command
class InsertCommand : public Command {
private:
    TextEditor& editor;
    std::string text;
public:
    InsertCommand(TextEditor& e, const std::string& t) : editor(e), text(t) {}
    void execute() override { editor.insertText(text); }
    void undo() override { editor.deleteText(text.length()); }
};

// Invoker
class CommandHistory {
private:
    std::vector<std::unique_ptr<Command>> executed;
    std::vector<std::unique_ptr<Command>> undone;
public:
    void execute(std::unique_ptr<Command> cmd) {
        cmd->execute();
        executed.push_back(std::move(cmd));
        undone.clear();
    }
    void undo() {
        if (!executed.empty()) {
            auto cmd = std::move(executed.back());
            executed.pop_back();
            cmd->undo();
            undone.push_back(std::move(cmd));
        }
    }
};

int main() {
    TextEditor editor;
    CommandHistory history;
    
    history.execute(std::make_unique<InsertCommand>(editor, "Hello "));
    history.execute(std::make_unique<InsertCommand>(editor, "World!"));
    editor.print();  // 'Hello World!'
    
    history.undo();
    editor.print();  // 'Hello '
}"""

BEFORE_CODE = r"""// Without Command - undo logic scattered everywhere
class TextEditor {
    string content;
    vector<string> history;
    
    void insert(string text) {
        history.push_back(content);
        content += text;
    }
    void undo() {
        if (!history.empty()) {
            content = history.back();
            history.pop_back();
        }
    }
    // Only supports insert, not other operations
}"""

AFTER_CODE = r"""// With Command - each action is a first-class object
class InsertCommand : public Command {
    void execute() override { editor.insert(text); }
    void undo() override { editor.delete(text.length()); }
};
// Easy to add new command types (DeleteCommand, PasteCommand, etc.)"""


def demonstrate() -> dict:
    """Execute the Command pattern demonstration."""
    return {
        "cpp_code": CPP_CODE,
        "before_code": BEFORE_CODE,
        "after_code": AFTER_CODE,
        "intent": (
            "Encapsulates a request as an object, thereby allowing parameterization "
            "of clients with different requests, queueing, logging, and undoable operations."
        ),
        "context": (
            "Text editor undo/redo - each action (insert, delete) is wrapped in a "
            "Command object that knows how to execute and undo itself."
        ),
        "pros": [
            "Decouples invoker from receiver",
            "Easy to implement undo/redo",
            "Commands can be composed into macro commands",
        ],
        "cons": [
            "Can lead to many small command classes",
            "Adds complexity for simple operations",
        ],
        "anti_pattern": (
            "Command Explosion: Avoid creating a separate command object for every "
            "tiny, atomic action. Group related operations or use a generic command "
            "with parameters when the per-action overhead isn't justified."
        ),
        "uml_diagram": """
┌─────────────────┐         ┌──────────────────┐
│ CommandHistory  │────────>│    Command       │
│   (Invoker)     │         │   (interface)    │
├─────────────────┤         ├──────────────────┤
│ -executed[]     │         │ +execute()       │
│ -undone[]       │         │ +undo()          │
├─────────────────┤         └────────┬─────────
│ +execute(cmd)   │           ┌──────┴──────┐
│ +undo()         │           ▼             ▼
│ +redo()         │    ┌──────────┐ ┌──────────┐
─────────────────┘    │InsertCmd │ │DeleteCmd │
                     ├──────────┤ ├──────────┤
                     │-editor   │ │-editor   │
                     │-text     │ │-position │
                     └──────────┘ └──────────┘
                          │           │
                          ▼           ▼
                     ┌──────────────────┐
                     │   TextEditor     │
                     │   (Receiver)     │
                     └──────────────────┘""",
    }
