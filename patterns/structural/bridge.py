"""Bridge Pattern Demonstration (C++).

Real-world context: Drawing application - decoupling Shape abstraction from
DrawingAPI implementation so both can vary independently.

Anti-pattern warning: Increased complexity - Using Bridge when there's only
one implementation, adding unnecessary indirection.
"""

CPP_CODE = r"""#include <iostream>
#include <memory>

// Implementor Interface
class DrawingAPI {
public:
    virtual void drawCircle(double x, double y, double radius) = 0;
    virtual ~DrawingAPI() = default;
};

// Concrete Implementor: DrawingAPIv1
class DrawingAPIv1 : public DrawingAPI {
public:
    void drawCircle(double x, double y, double radius) override {
        std::cout << "API v1: Circle at (" << x << "," << y 
                  << ") radius=" << radius << "\n";
    }
};

// Concrete Implementor: DrawingAPIv2
class DrawingAPIv2 : public DrawingAPI {
public:
    void drawCircle(double x, double y, double radius) override {
        std::cout << "API v2: Circle at (" << x << "," << y 
                  << ") radius=" << radius << "\n";
    }
};

// Refined Abstraction
class CircleShape {
protected:
    double x, y, radius;
    std::unique_ptr<DrawingAPI> drawingAPI;

public:
    CircleShape(double x, double y, double r, std::unique_ptr<DrawingAPI> api)
        : x(x), y(y), radius(r), drawingAPI(std::move(api)) {}

    virtual void draw() {
        drawingAPI->drawCircle(x, y, radius);
    }
    
    virtual void resize(double factor) {
        radius *= factor;
    }
};

// Example usage
int main() {
    auto v1api = std::make_unique<DrawingAPIv1>();
    auto v2api = std::make_unique<DrawingAPIv2>();

    CircleShape circle1(1, 2, 3, std::move(v1api));
    CircleShape circle2(5, 7, 10, std::move(v2api));

    circle1.draw();
    circle2.draw();
    
    circle2.resize(1.5);
    circle2.draw();
}"""

BEFORE_CODE = r"""// Without Bridge - tightly coupled inheritance
class OpenGLCircle {
    void draw() { /* OpenGL specific */ }
};

class DirectXCirlce {
    void draw() { /* DirectX specific */ }
};
// Adding new shape requires new class for each API"""

AFTER_CODE = r"""// With Bridge - composition over inheritance
class CircleShape {
    std::unique_ptr<DrawingAPI> api;
    void draw() { api->drawCircle(x, y, radius); }
};
// Shape and API vary independently"""


def demonstrate() -> dict:
    """Execute the Bridge pattern demonstration."""
    return {
        "cpp_code": CPP_CODE,
        "before_code": BEFORE_CODE,
        "after_code": AFTER_CODE,
        "intent": (
            "Decouples an abstraction from its implementation so the two can "
            "vary independently. Uses composition instead of inheritance."
        ),
        "context": (
            "Drawing application - Shape abstraction (Circle, Square) separated "
            "from rendering API (OpenGL, DirectX, Vulkan)."
        ),
        "pros": [
            "Abstraction and implementation can be extended independently",
            "Implementation details hidden from client code",
            "Avoids compile-time dependencies",
        ],
        "cons": [
            "Increases complexity by introducing additional abstraction layer",
            "Double indirection may impact performance slightly",
        ],
        "anti_pattern": (
            "Unnecessary Complexity: Don't use Bridge when there's only one "
            "implementation. The added indirection is only justified when "
            "multiple implementations exist or are planned."
        ),
        "uml_diagram": """
┌─────────────────┐     ┌─────────────────┐
│   CircleShape   │────>│   DrawingAPI    │
├─────────────────┤     ├─────────────────┤
│ -x, y, radius   │     │ +drawCircle()   │
│ -drawingAPI     │     └─────────────────┘
│ +draw()         │              ▲
│ +resize()       │       ┌──────┴──────┐
└─────────────────┘       ▼             ▼
                    ┌──────────┐  ┌──────────┐
                    │ API v1   │  │ API v2   │
                    └──────────┘  └──────────┘""",
    }
