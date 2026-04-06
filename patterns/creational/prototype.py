"""Prototype Pattern Demonstration (C++).

Real-world context: Game development - spawning hundreds of similar enemy units
by cloning pre-configured prototypes instead of creating from scratch.

Anti-pattern warning: Shallow copy issues - Failing to properly deep-copy
nested objects leads to shared references and bugs.
"""

CPP_CODE = r"""#include <iostream>
#include <memory>
#include <vector>

// Abstract Prototype
class Unit {
public:
    virtual ~Unit() = default;
    virtual std::unique_ptr<Unit> clone() const = 0;
    virtual void display() const = 0;
};

// Concrete Prototype: Archer
class Archer : public Unit {
private:
    int health;
    int damage;

public:
    Archer(int h = 100, int d = 20) : health(h), damage(d) {}
    
    std::unique_ptr<Unit> clone() const override {
        return std::make_unique<Archer>(*this);
    }
    
    void display() const override {
        std::cout << "Archer: HP=" << health << ", DMG=" << damage << "\n";
    }
};

// Concrete Prototype: Knight
class Knight : public Unit {
private:
    int health;
    int damage;
    bool isMounted;

public:
    Knight(int h = 150, int d = 30, bool mounted = true) 
        : health(h), damage(d), isMounted(mounted) {}
    
    std::unique_ptr<Unit> clone() const override {
        return std::make_unique<Knight>(*this);
    }
    
    void display() const override {
        std::cout << "Knight: HP=" << health << ", DMG=" << damage 
                  << ", " << (isMounted ? "mounted" : "on foot") << "\n";
    }
};

// Prototype Manager
class UnitFactory {
private:
    std::vector<std::unique_ptr<Unit>> prototypes;

public:
    UnitFactory() {
        prototypes.push_back(std::make_unique<Archer>(100, 25));
        prototypes.push_back(std::make_unique<Knight>(200, 35, true));
    }
    
    std::unique_ptr<Unit> createUnit(int index) {
        if (index >= 0 && index < prototypes.size()) {
            return prototypes[index]->clone();
        }
        return nullptr;
    }
};

int main() {
    UnitFactory factory;
    
    auto archer1 = factory.createUnit(0);
    auto knight1 = factory.createUnit(1);
    auto archer2 = factory.createUnit(0);
    
    archer1->display();
    knight1->display();
    archer2->display();
}"""

BEFORE_CODE = r"""// Without Prototype - creating each unit from scratch
Archer* createArcher(int level) {
    Archer* a = new Archer();
    a->setHealth(100 + level * 10);
    a->setDamage(20 + level * 5);
    a->setEquipment(loadEquipment("archer"));
    a->setAnimations(loadAnimations("archer"));
    // Expensive: loads assets every time
    return a;
}"""

AFTER_CODE = r"""// With Prototype - cloning pre-configured prototype
Archer* createArcher(int level) {
    Archer* clone = prototype->clone();
    clone->scaleStats(level);
    // Fast: copy already-loaded assets
    return clone;
}"""


def demonstrate() -> dict:
    """Execute the Prototype pattern demonstration.

    Returns:
        Dictionary containing demonstration output data.
    """
    return {
        "cpp_code": CPP_CODE,
        "before_code": BEFORE_CODE,
        "after_code": AFTER_CODE,
        "intent": (
            "Allows copying existing objects without making code dependent on "
            "their classes. Ideal when object creation is expensive."
        ),
        "context": (
            "Game development - spawning enemy units by cloning pre-configured "
            "prototypes instead of loading assets from scratch each time."
        ),
        "pros": [
            "Reduces subclass proliferation",
            "Avoids expensive initialization by cloning configured objects",
            "Runtime addition/removal of prototypes",
        ],
        "cons": [
            "Deep copying complex objects with circular references is tricky",
            "Each subclass must implement clone() method",
        ],
        "anti_pattern": (
            "Shallow Copy Issues: Failing to properly deep-copy nested objects "
            "leads to shared references. Ensure clone() performs deep copies of "
            "all owned resources."
        ),
        "uml_diagram": """
┌──────────────────────┐
│       Unit           │
├──────────────────────┤
│ +clone() const       │
│ +display() const     │
└──────────────────────┘
          ▲
    ┌─────┴─────┐
    ▼           ▼
┌────────┐  ┌────────┐
│ Archer │  │ Knight │
├────────┤  ├────────┤
│ health │  │ health │
│ damage │  │ damage │
│        │  │mounted │
└────────┘  └────────┘

┌──────────────────────┐
│    UnitFactory       │
├──────────────────────┤
│ -prototypes[]        │
│ +createUnit(idx)     │
└──────────────────────┘""",
    }
