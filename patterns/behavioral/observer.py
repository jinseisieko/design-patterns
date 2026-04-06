"""Observer Pattern Demonstration (C++).

Real-world context: When a background job completes, it notifies registered
observers (email sender, logger, cache invalidator) about the event.

Anti-pattern warning: Memory Leaks - Failing to detach observers from a subject,
causing them to remain in memory indefinitely.
"""

CPP_CODE = r"""#include <iostream>
#include <vector>
#include <memory>
#include <string>
#include <algorithm>

// Observer Interface
class Observer {
public:
    virtual ~Observer() = default;
    virtual void update(const std::string& event) = 0;
};

// Subject
class JobStatusPublisher {
private:
    std::vector<std::unique_ptr<Observer>> observers;
public:
    void attach(std::unique_ptr<Observer> obs) {
        observers.push_back(std::move(obs));
    }
    void detach(Observer* toRemove) {
        observers.erase(
            std::remove_if(observers.begin(), observers.end(),
                [toRemove](const auto& o) { return o.get() == toRemove; }),
            observers.end());
    }
    void notify(const std::string& event) {
        for (const auto& obs : observers)
            obs->update(event);
    }
};

// Concrete Observers
class EmailNotifier : public Observer {
public:
    void update(const std::string& event) override {
        std::cout << "Email: Sending notification for '" << event << "'\n";
    }
};

class CacheInvalidator : public Observer {
public:
    void update(const std::string& event) override {
        if (event == "JOB_COMPLETED")
            std::cout << "Cache: Invalidating cache for completed job\n";
    }
};

class AuditLogger : public Observer {
public:
    void update(const std::string& event) override {
        std::cout << "Audit: Logging event '" << event << "'\n";
    }
};

int main() {
    JobStatusPublisher publisher;
    
    publisher.attach(std::make_unique<EmailNotifier>());
    publisher.attach(std::make_unique<CacheInvalidator>());
    publisher.attach(std::make_unique<AuditLogger>());
    
    publisher.notify("JOB_STARTED");
    publisher.notify("JOB_COMPLETED");
    
    // Detach email notifier
    // publisher.detach(&emailNotifier);
}"""

BEFORE_CODE = r"""// Without Observer - hardcoded notifications
class JobRunner {
    void onComplete() {
        emailService->send("Job done");
        cacheService->invalidate();
        auditLog->write("Job done");
        // Tightly coupled to all notification services
    }
}"""

AFTER_CODE = r"""// With Observer - decoupled notifications
class JobRunner {
    void onComplete() {
        publisher->notify("JOB_COMPLETED");
        // Doesn't know who the observers are
    }
}"""


def demonstrate() -> dict:
    """Execute the Observer pattern demonstration."""
    return {
        "cpp_code": CPP_CODE,
        "before_code": BEFORE_CODE,
        "after_code": AFTER_CODE,
        "intent": (
            "Defines a one-to-many dependency between objects so that when one object "
            "changes state, all its dependents are notified and updated automatically."
        ),
        "context": (
            "Background job notifications - when a job completes, it notifies "
            "email sender, logger, and cache invalidator without knowing about them."
        ),
        "pros": [
            "Loose coupling between subject and observers",
            "Easy to add/remove observers at runtime",
            "Supports broadcast communication",
        ],
        "cons": [
            "Observers notified in unpredictable order",
            "Memory leaks if observers aren't detached",
        ],
        "anti_pattern": (
            "Memory Leaks: Always detach observers when they're no longer needed. "
            "Consider using std::weak_ptr for automatic cleanup and to prevent "
            "circular references between subject and observers."
        ),
        "uml_diagram": """
┌────────────────────────┐         ┌──────────────────┐
│ JobStatusPublisher     │────────>│    Observer      │
│      (Subject)         │         │   (interface)    │
├────────────────────────┤         ├──────────────────┤
│ -observers[]           │         │ +update(event)   │
├────────────────────────┤         └────────┬─────────┘
│ +attach(observer)      │           ┌──────┼──────┐
│ +detach(observer)      │           ▼      ▼      ▼
│ +notify(event)         │    ┌────────┐ ┌────┐ ┌────┐
────────────────────────┘    │ Email  │ │Cache│ │Audit│
                              │Notifier│ │Inv. │ │Logger│
                              └────────┘ └─────┘ └─────┘""",
    }
