"""Factory Method Pattern Demonstration (C++).

Real-world context: Payment processing gateway - delegating the creation of
different payment processors to subclasses.

Anti-pattern warning: Complexity Overhead - Using a factory where a simple
constructor would suffice for trivial object creation.
"""

CPP_CODE = r"""#include <iostream>
#include <memory>

// Product Interface
class PaymentProcessor {
public:
    virtual void processPayment(double amount) = 0;
    virtual ~PaymentProcessor() = default;
};

// Concrete Product: CreditCardProcessor
class CreditCardProcessor : public PaymentProcessor {
public:
    void processPayment(double amount) override {
        std::cout << "Processing $" << amount << " via Credit Card.\n";
    }
};

// Concrete Product: PayPalProcessor
class PayPalProcessor : public PaymentProcessor {
public:
    void processPayment(double amount) override {
        std::cout << "Processing $" << amount << " via PayPal.\n";
    }
};

// Creator Class
class PaymentGateway {
public:
    // Factory Method
    virtual std::unique_ptr<PaymentProcessor> createProcessor() = 0;
    
    // Business Logic using the factory method
    void executePayment(double amount) {
        auto processor = createProcessor();
        processor->processPayment(amount);
    }
    
    virtual ~PaymentGateway() = default;
};

// Concrete Creator: CreditCardGateway
class CreditCardGateway : public PaymentGateway {
public:
    std::unique_ptr<PaymentProcessor> createProcessor() override {
        return std::make_unique<CreditCardProcessor>();
    }
};

// Concrete Creator: PayPalGateway
class PayPalGateway : public PaymentGateway {
public:
    std::unique_ptr<PaymentProcessor> createProcessor() override {
        return std::make_unique<PayPalProcessor>();
    }
};

int main() {
    std::unique_ptr<PaymentGateway> gateway;

    gateway = std::make_unique<CreditCardGateway>();
    gateway->executePayment(100.50);

    gateway = std::make_unique<PayPalGateway>();
    gateway->executePayment(250.75);
}"""

BEFORE_CODE = r"""// Without Factory Method - hardcoded creation
class PaymentService {
    void pay(const string& type, double amount) {
        if (type == "credit") {
            CreditCardProcessor* p = new CreditCardProcessor();
            p->process(amount);
        } else if (type == "paypal") {
            PayPalProcessor* p = new PayPalProcessor();
            p->process(amount);
        }
        // Hard to add new payment types
    }
}"""

AFTER_CODE = r"""// With Factory Method - subclasses decide
class PaymentGateway {
    virtual unique_ptr<Processor> createProcessor() = 0;
    void execute(double amount) {
        createProcessor()->process(amount);
    }
};
// Easy to add new gateways by subclassing"""


def demonstrate() -> dict:
    """Execute the Factory Method pattern demonstration."""
    return {
        "cpp_code": CPP_CODE,
        "before_code": BEFORE_CODE,
        "after_code": AFTER_CODE,
        "intent": (
            "Lets a class delegate the responsibility of instantiating itself to "
            "its subclasses via a factory method."
        ),
        "context": (
            "Payment processing gateway - creating different payment processors "
            "(Credit Card, PayPal) based on the gateway type."
        ),
        "pros": [
            "Eliminates tight coupling between creator and concrete products",
            "Open-Closed Principle: add new products without modifying creator",
            "Single Responsibility: creation logic isolated in subclasses",
        ],
        "cons": [
            "Can lead to large number of subclasses",
            "Complexity overhead for simple object creation",
        ],
        "anti_pattern": (
            "Complexity Overhead: Don't use Factory Method where a simple "
            "constructor or direct instantiation would suffice. Reserve it for "
            "cases where subclasses genuinely need to control object creation."
        ),
        "uml_diagram": """
┌────────────────────────┐
│    PaymentGateway      │
│    (Creator)           │
├────────────────────────┤
│ +createProcessor()     │
│ +executePayment()      │
└───────────┬────────────┘
            │
      ┌─────┴────────┐
      ▼              ▼
┌────────────┐ ┌────────────
│CreditCard  │ │   PayPal   │
│  Gateway   │ │   Gateway  │
└────────────┘ └────────────┘
      │              │
      ▼              ▼
┌──────────── ┌────────────┐
│CreditCard  │ │   PayPal   │
│ Processor  │ │  Processor │
└────────────┘ └────────────""",
    }
