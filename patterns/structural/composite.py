"""Composite Pattern Demonstration (C++).

Real-world context: Graphical scene graphs - composing objects into tree structures
to represent part-whole hierarchies, treating individuals and compositions uniformly.

Anti-pattern warning: Overly general interface - Making leaf-specific operations
available on composite classes, leading to runtime errors.
"""

CPP_CODE = r"""#include <iostream>
#include <vector>
#include <memory>

// Component Interface
class Graphic {
public:
    virtual void move(int x, int y) = 0;
    virtual void draw() = 0;
    virtual ~Graphic() = default;
};

// Leaf
class Dot : public Graphic {
private:
    int x, y;
public:
    Dot(int x, int y) : x(x), y(y) {}
    void move(int dx, int dy) override { x += dx; y += dy; }
    void draw() override {
        std::cout << "  Dot at (" << x << "," << y << ")\n";
    }
};

// Composite
class CompoundGraphic : public Graphic {
private:
    std::vector<std::unique_ptr<Graphic>> children;
public:
    void add(std::unique_ptr<Graphic> g) {
        children.push_back(std::move(g));
    }
    void move(int dx, int dy) override {
        for (auto& child : children) {
            child->move(dx, dy);
        }
    }
    void draw() override {
        std::cout << "Compound Graphic:\n";
        for (auto& child : children) {
            child->draw();
        }
    }
};

int main() {
    auto p1 = std::make_unique<Dot>(1, 2);
    auto p2 = std::make_unique<Dot>(3, 4);
    auto p3 = std::make_unique<Dot>(5, 6);

    auto group = std::make_unique<CompoundGraphic>();
    group->add(std::move(p1));
    group->add(std::move(p2));

    auto rootGroup = std::make_unique<CompoundGraphic>();
    rootGroup->add(std::move(p3));
    rootGroup->add(std::move(group));

    rootGroup->draw();
}"""

BEFORE_CODE = r"""// Without Composite - treating leaves and composites differently
void renderScene(std::vector<Dot*>& dots, std::vector<Group*>& groups) {
    for (auto dot : dots) {
        dot->draw();
    }
    for (auto group : groups) {
        for (auto child : group->getChildren()) {
            child->draw();  // Different logic for each type
        }
    }
}"""

AFTER_CODE = r"""// With Composite - uniform treatment
void renderScene(Graphic* graphic) {
    graphic->draw();  // Works for both leaves and composites
}"""


def demonstrate() -> dict:
    """Execute the Composite pattern demonstration."""
    return {
        "cpp_code": CPP_CODE,
        "before_code": BEFORE_CODE,
        "after_code": AFTER_CODE,
        "intent": (
            "Composes objects into tree structures to represent part-whole "
            "hierarchies. Lets clients treat individual objects and compositions uniformly."
        ),
        "context": (
            "Scene graphs in graphics applications - uniform treatment of "
            "primitive shapes and groups of shapes."
        ),
        "pros": [
            "Simplifies client code - no need to distinguish leaf vs composite",
            "Easy to add new component types",
            "Recursive composition enables complex structures",
        ],
        "cons": [
            "Can make design overly general if interface is too broad",
            "Leaf-specific operations may be awkward on composites",
        ],
        "anti_pattern": (
            "Overly General Interface: Don't expose leaf-specific operations "
            "on composite classes. Use runtime checks or separate interfaces "
            "when operations don't apply to all components."
        ),
        "uml_diagram": """
┌─────────────────────┐
│      Graphic        │
├─────────────────────┤
│ +move(x, y)         │
│ +draw()             │
└─────────────────────┘
          ▲
    ┌─────┴────────────┐
    ▼                  ▼
┌────────┐    ┌───────────────────┐
│  Dot   │    │CompoundGraphic    │
├────────┤    ├───────────────────┤
│ x, y   │    │ -children[]       │
└────────┘    │ +add(Graphic)     │
              │ +move(x, y)       │
              │ +draw()           │
              └───────────────────┘
                     │
                     ▼ (recursive)
              ┌───────────────────┐
              │Graphic children...│
              └───────────────────┘""",
    }
