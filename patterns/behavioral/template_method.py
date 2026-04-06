"""Template Method Pattern Demonstration (C++).

Real-world context: Game character turn processing - defining the skeleton of
an algorithm in a base class, deferring steps to subclasses.

Anti-pattern warning: Callback hell - Too many hook methods making the template
difficult to understand and maintain.
"""

CPP_CODE = r"""#include <iostream>
#include <memory>

// Abstract Class (Base Class)
class GameCharacter {
public:
    // Template Method - defines algorithm skeleton
    void playTurn() {
        std::cout << "=== Starting Turn ===\n";
        prepareAction();
        executeAction();
        endTurn();
    }
    
protected:
    // Hook: optional override
    virtual void prepareAction() {
        std::cout << "Preparing generic action.\n";
    }
    
    // Abstract step: must override
    virtual void executeAction() = 0;
    
    // Hook: optional override
    virtual void endTurn() {
        std::cout << "Ending turn.\n";
    }
    
    virtual ~GameCharacter() = default;
};

// Concrete Class 1
class Warrior : public GameCharacter {
protected:
    void prepareAction() override {
        std::cout << "Warrior sharpens weapon.\n";
    }
    void executeAction() override {
        std::cout << "Warrior swings sword! [-30 HP]\n";
    }
};

// Concrete Class 2
class Mage : public GameCharacter {
protected:
    void prepareAction() override {
        std::cout << "Mage chants spell.\n";
    }
    void executeAction() override {
        std::cout << "Mage casts Fireball! [-50 HP]\n";
    }
    void endTurn() override {
        std::cout << "Mage recovers mana. Ending turn.\n";
    }
};

int main() {
    std::unique_ptr<GameCharacter> warrior = std::make_unique<Warrior>();
    std::unique_ptr<GameCharacter> mage = std::make_unique<Mage>();
    
    std::cout << "\nWarrior's turn:\n";
    warrior->playTurn();
    
    std::cout << "\nMage's turn:\n";
    mage->playTurn();
}"""

BEFORE_CODE = r"""// Without Template Method - duplicated algorithm
void warriorTurn() {
    prepareWarrior();
    warriorAttack();
    cleanupWarrior();
}

void mageTurn() {
    prepareMage();
    mageCastSpell();
    recoverMana();
}
// Same structure, duplicated code"""

AFTER_CODE = r"""// With Template Method - shared algorithm structure
class GameCharacter {
    void playTurn() {  // Fixed algorithm
        prepareAction();  // customizable
        executeAction();  // must override
        endTurn();        // customizable
    }
};"""


def demonstrate() -> dict:
    """Execute the Template Method pattern demonstration."""
    return {
        "cpp_code": CPP_CODE,
        "before_code": BEFORE_CODE,
        "after_code": AFTER_CODE,
        "intent": (
            "Defines the skeleton of an algorithm in a method, deferring some steps "
            "to subclasses. Lets subclasses redefine certain steps without changing "
            "the algorithm's structure."
        ),
        "context": (
            "Game character turns - fixed turn structure (prepare, execute, end) "
            "with character-specific implementations."
        ),
        "pros": [
            "Code reuse: common algorithm in one place",
            "Inversion of Control: framework calls your code",
            "Easy to add new variants by subclassing",
        ],
        "cons": [
            "Subclasses must understand template method contract",
            "Too many hook methods make template hard to follow",
            "Debugging can be harder with scattered implementations",
        ],
        "anti_pattern": (
            "Callback Hell: Don't add too many hook methods. If the template has "
            "more hooks than actual steps, consider a different design like "
            "Strategy or Builder."
        ),
        "uml_diagram": """
┌─────────────────────────┐
│     GameCharacter       │
├─────────────────────────┤
│ +playTurn()             │  <-- Template Method
│   prepareAction()       │  <-- Hook (optional)
│   executeAction() = 0   │  <-- Abstract (required)
│   endTurn()             │  <-- Hook (optional)
└───────────┬─────────────┘
            │
      ┌─────┴─────┐
      ▼           ▼
┌──────────┐  ┌──────────┐
│ Warrior  │  │   Mage   │
├──────────┤  ├──────────┤
│prepare() │  │prepare() │
│execute() │  │execute() │
│          │  │endTurn() │
└──────────┘  └──────────┘""",
    }
