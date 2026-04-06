"""Interpreter Pattern Demonstration (C++).

Real-world context: Mathematical expression evaluator - defining a grammar
representation and interpreter for evaluating expressions.

Anti-pattern warning: Complex grammar - For complex languages, dedicated parser
generators (ANTLR, Boost.Spirit) are better than manual Interpreter implementation.
"""

CPP_CODE = r"""#include <iostream>
#include <memory>
#include <string>

// Abstract Expression
class Expression {
public:
    virtual ~Expression() = default;
    virtual int interpret() = 0;
};

// Terminal: Number
class NumberExpression : public Expression {
private:
    int value;
public:
    explicit NumberExpression(int v) : value(v) {}
    int interpret() override { return value; }
};

// Non-terminal: Addition
class AddExpression : public Expression {
private:
    std::unique_ptr<Expression> left, right;
public:
    AddExpression(std::unique_ptr<Expression> l, std::unique_ptr<Expression> r)
        : left(std::move(l)), right(std::move(r)) {}
    int interpret() override {
        return left->interpret() + right->interpret();
    }
};

// Non-terminal: Subtraction
class SubtractExpression : public Expression {
private:
    std::unique_ptr<Expression> left, right;
public:
    SubtractExpression(std::unique_ptr<Expression> l, std::unique_ptr<Expression> r)
        : left(std::move(l)), right(std::move(r)) {}
    int interpret() override {
        return left->interpret() - right->interpret();
    }
};

int main() {
    // Build AST for: (5 + 3) - 2
    auto expr = std::make_unique<SubtractExpression>(
        std::make_unique<AddExpression>(
            std::make_unique<NumberExpression>(5),
            std::make_unique<NumberExpression>(3)
        ),
        std::make_unique<NumberExpression>(2)
    );
    
    std::cout << "Result: " << expr->interpret() << "\n"; // Output: 6
}"""

BEFORE_CODE = r"""// Without Interpreter - hardcoded evaluation
int evaluate(const string& expr) {
    if (expr == "5+3-2") return 6;
    if (expr == "10*2+1") return 21;
    // Not extensible, doesn't parse
}"""

AFTER_CODE = r"""// With Interpreter - composable expression tree
auto expr = make_unique<SubtractExpr>(
    make_unique<AddExpr>(num(5), num(3)),
    num(2)
);
expr->interpret(); // Returns 6"""


def demonstrate() -> dict:
    """Execute the Interpreter pattern demonstration."""
    return {
        "cpp_code": CPP_CODE,
        "before_code": BEFORE_CODE,
        "after_code": AFTER_CODE,
        "intent": (
            "Defines a representation for a grammar and an interpreter to evaluate "
            "sentences in that language."
        ),
        "context": (
            "Mathematical expression evaluator - building and evaluating "
            "abstract syntax trees for arithmetic operations."
        ),
        "pros": [
            "Easy to change and extend the grammar",
            "Each grammar rule is a separate class",
            "Straightforward implementation for simple languages",
        ],
        "cons": [
            "Complex grammars create many small classes",
            "Hard to maintain for complex grammars",
            "Modern parser generators are more efficient",
        ],
        "anti_pattern": (
            "Complex Grammar: For complex languages, use dedicated parser "
            "generators like ANTLR or Boost.Spirit instead of manual Interpreter. "
            "The pattern is only practical for simple grammars."
        ),
        "uml_diagram": """
┌─────────────────┐
│   Expression    │
├─────────────────┤
│ +interpret()    │
└────────┬────────┘
         │
    ┌────┼──────────────┐
    ▼    ▼              ▼
┌──────┐ ┌────────┐ ┌──────────┐
│Number│ │ Add    │ │ Subtract │
├──────┤ ├────────┤ ├──────────┤
│-value│ │-left   │ │-left     │
│      │ │-right  │ │-right    │
└──────┘ └────────┘ └──────────┘
                    (recursive structure)""",
    }
