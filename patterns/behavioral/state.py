"""State Pattern Demonstration (C++).

Real-world context: E-commerce order lifecycle - the order's behavior changes
based on its current state (Pending, Shipped, Delivered).

Anti-pattern warning: State-Space Explosion - Modeling too many states leading
to a complex web of state classes that is hard to manage.
"""

CPP_CODE = r"""#include <iostream>
#include <memory>
#include <string>

// Forward declaration
class Order;

// State Interface
class OrderState {
public:
    virtual ~OrderState() = default;
    virtual void handle(Order& order) = 0;
    virtual std::string getName() const = 0;
};

// Concrete States
class PendingState : public OrderState {
public:
    std::string getName() const override { return "Pending"; }
    void handle(Order& order) override;
};

class ShippedState : public OrderState {
public:
    std::string getName() const override { return "Shipped"; }
    void handle(Order& order) override;
};

class DeliveredState : public OrderState {
public:
    std::string getName() const override { return "Delivered"; }
    void handle(Order& order) override;
};

// Context
class Order {
private:
    std::unique_ptr<OrderState> state;
    int id;
public:
    explicit Order(int orderId) : id(orderId) {
        state = std::make_unique<PendingState>();
    }
    
    void setState(std::unique_ptr<OrderState> newState) {
        std::cout << "Order #" << id << ": " 
                  << state->getName() << " -> " 
                  << newState->getName() << "\n";
        state = std::move(newState);
    }
    
    void nextState() { state->handle(*this); }
    std::string getStateName() const { return state->getName(); }
    int getId() const { return id; }
};

// State implementations
void PendingState::handle(Order& order) {
    std::cout << "Order #" << order.getId() << " is pending. Processing...\n";
    order.setState(std::make_unique<ShippedState>());
}

void ShippedState::handle(Order& order) {
    std::cout << "Order #" << order.getId() << " shipped. Tracking...\n";
    order.setState(std::make_unique<DeliveredState>());
}

void DeliveredState::handle(Order& order) {
    std::cout << "Order #" << order.getId() << " delivered. Complete!\n";
}

int main() {
    Order order(1001);
    
    std::cout << "=== Order Lifecycle ===\n";
    for (int i = 0; i < 4; ++i) {
        order.nextState();
    }
}"""

BEFORE_CODE = r"""// Without State - switch statement spaghetti
class Order {
    enum Status { PENDING, SHIPPED, DELIVERED };
    Status status;
    
    void nextState() {
        switch (status) {
            case PENDING:
                process(); status = SHIPPED; break;
            case SHIPPED:
                track(); status = DELIVERED; break;
            case DELIVERED:
                // Nothing to do
                break;
        }
    }
    // Adding new state requires modifying this switch
}"""

AFTER_CODE = r"""// With State - each state is a class
class Order {
    unique_ptr<OrderState> state;
    void nextState() { state->handle(*this); }
};

class ShippedState : public OrderState {
    void handle(Order& o) {
        // shipped logic
        o.setState(make_unique<DeliveredState>());
    }
};"""


def demonstrate() -> dict:
    """Execute the State pattern demonstration."""
    return {
        "cpp_code": CPP_CODE,
        "before_code": BEFORE_CODE,
        "after_code": AFTER_CODE,
        "intent": (
            "Allows an object to alter its behavior when its internal state changes. "
            "The object appears to change its class."
        ),
        "context": (
            "E-commerce order lifecycle - the order transitions from Pending to "
            "Shipped to Delivered, with different behavior at each stage."
        ),
        "pros": [
            "Eliminates large switch/if-else statements",
            "Single Responsibility: each state class has one concern",
            "Open-Closed: add new states without modifying context",
        ],
        "cons": [
            "Increases number of classes",
            "Can be overkill for simple state machines",
        ],
        "anti_pattern": (
            "State-Space Explosion: Avoid modeling too many states for an object. "
            "If you have more than 5-7 states, consider whether a state machine "
            "library or a simpler approach would be more manageable."
        ),
        "uml_diagram": """
┌─────────────────┐         ┌──────────────────┐
│     Order       │────────>│   OrderState     │
│   (Context)     │         │   (interface)    │
├─────────────────┤         ├──────────────────┤
│ -state          │         │ +handle(order)   │
├─────────────────┤         │ +getName()       │
│ +nextState()    │         └────────┬─────────
│ +setState()     │           ┌──────┼──────┐
└─────────────────┘           ▼      ▼      ▼
                        ┌────────┐ ┌──────┐ ┌──────────┐
                        │Pending │ │Ship. │ │Delivered │
                        │ State  │ │State │ │  State   │
                        └────────┘ └──────┘ └──────────""",
    }
