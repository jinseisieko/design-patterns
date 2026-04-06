"""Visitor Pattern Demonstration (C++).

Real-world context: AST traversal in compiler - separating algorithms from object
structure, allowing new operations without changing element classes.

Anti-pattern warning: Breaking encapsulation - Visitor accessing private members
of elements, violating information hiding.
"""

CPP_CODE = r"""#include <iostream>
#include <memory>

// Forward declarations
class BinaryExpr;
class Literal;

// Visitor Interface
class Visitor {
public:
    virtual ~Visitor() = default;
    virtual int visit(const Literal& lit) = 0;
    virtual int visit(const BinaryExpr& expr) = 0;
};

// Element Interface
class Expr {
public:
    virtual ~Expr() = default;
    virtual int accept(Visitor& v) const = 0;
};

// Concrete Element: Literal
class Literal : public Expr {
public:
    int value;
    explicit Literal(int v) : value(v) {}
    int accept(Visitor& v) const override { return v.visit(*this); }
};

// Concrete Element: BinaryExpr
class BinaryExpr : public Expr {
public:
    std::unique_ptr<Expr> left, right;
    char op;
    BinaryExpr(std::unique_ptr<Expr> l, char o, std::unique_ptr<Expr> r)
        : left(std::move(l)), op(o), right(std::move(r)) {}
    int accept(Visitor& v) const override { return v.visit(*this); }
};

// Concrete Visitor: Evaluator
class Evaluator : public Visitor {
public:
    int visit(const Literal& lit) override { return lit.value; }
    
    int visit(const BinaryExpr& expr) override {
        int l = expr.left->accept(*this);
        int r = expr.right->accept(*this);
        switch (expr.op) {
            case '+': return l + r;
            case '-': return l - r;
            case '*': return l * r;
            default: return 0;
        }
    }
};

int main() {
    // AST: (1 + 2) * 3
    auto ast = std::make_unique<BinaryExpr>(
        std::make_unique<BinaryExpr>(
            std::make_unique<Literal>(1), '+',
            std::make_unique<Literal>(2)
        ),
        '*',
        std::make_unique<Literal>(3)
    );
    
    Evaluator eval;
    std::cout << "Result: " << ast->accept(eval) << "\n"; // 9
}"""

BEFORE_CODE = r"""// Without Visitor - operations mixed with elements
class BinaryExpr {
    int evaluate() { return left->evaluate() op right->evaluate(); }
    string print() { return left->print() + op + right->print(); }
    bool validate() { /* validation logic */ }
    // Every new operation requires modifying all classes
}"""

AFTER_CODE = r"""// With Visitor - operations separated
class BinaryExpr {
    int accept(Visitor& v) { return v.visit(*this); }
};

class Evaluator : Visitor { /* evaluation logic */ }
class Printer : Visitor { /* printing logic */ }
// New operations don't require changing elements"""


def demonstrate() -> dict:
    """Execute the Visitor pattern demonstration."""
    return {
        "cpp_code": CPP_CODE,
        "before_code": BEFORE_CODE,
        "after_code": AFTER_CODE,
        "intent": (
            "Separates an algorithm from the object structure on which it operates. "
            "Allows defining new operations without changing element classes."
        ),
        "context": (
            "AST traversal in compiler - evaluating, printing, validating "
            "expression trees without modifying node classes."
        ),
        "pros": [
            "Easy to add new operations without changing elements",
            "Related operations are grouped in single visitor class",
            "Visitor can accumulate state across traversal",
        ],
        "cons": [
            "Hard to add new element types (must update all visitors)",
            "Breaking encapsulation if visitor needs private access",
            "Complex double-dispatch mechanism",
        ],
        "anti_pattern": (
            "Breaking Encapsulation: Don't let visitors access private members "
            "of elements. If a visitor needs internal data, expose it through "
            "public interface or reconsider the design."
        ),
        "uml_diagram": """
┌─────────────────┐     ┌─────────────────┐
│    Visitor      │     │      Expr       │
├─────────────────┤     ├─────────────────┤
│ +visit(Literal) │     │ +accept(Visitor)│
│ +visit(Binary)  │     └────────┬────────┘
└────────┬────────┘              ▲
         │                 ┌─────┼──────┐
    ┌────┼────┐            ▼            ▼
    ▼         ▼      ┌──────────┐ ┌──────────┐
┌────────┐ ┌────────┐│ Literal  │ │BinaryExpr│
│Evaluator│ │Printer │├──────────┤ ├──────────┤
└────────┘ └────────┘│ -value   │ │-left,right│
                     └──────────┘ │-op       │
                                  └──────────┘""",
    }
