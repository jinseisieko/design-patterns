"""Singleton Pattern Demonstration (C++).

Real-world context: A logging service that ensures only one instance exists
throughout the application's lifecycle, preventing resource contention.

Anti-pattern warning: God Object - Creating a singleton that manages too many
unrelated responsibilities, violating the Single Responsibility Principle.
"""

CPP_CODE = r"""#include <iostream>
#include <mutex>
#include <string>

// Logger Singleton
class Logger {
private:
    // Private constructor prevents external instantiation
    Logger() {
        std::cout << "Logger instance created.\n";
    }

public:
    // Deleted copy constructor and assignment operator prevent copying
    Logger(const Logger&) = delete;
    Logger& operator=(const Logger&) = delete;

    // Static method to provide global access point (thread-safe since C++11)
    static Logger& getInstance() {
        static Logger instance;
        return instance;
    }

    void log(const std::string& message) {
        std::cout << "[LOG] " << message << "\n";
    }
};

int main() {
    Logger& logger1 = Logger::getInstance();
    Logger& logger2 = Logger::getInstance();

    logger1.log("Application started");
    logger2.log("User logged in");

    // Verify same instance
    if (&logger1 == &logger2) {
        std::cout << "Both references point to the same instance.\n";
    }
}"""

BEFORE_CODE = r"""// Without Singleton - multiple logger instances
class Logger {
public:
    void log(string msg) { /* write to file */ }
};

void handleRequest() {
    Logger logger1;
    logger1.log("Request received");
}

void processResponse() {
    Logger logger2;  // Different instance!
    logger2.log("Response sent");
}
// Logs may be scattered across multiple files"""

AFTER_CODE = r"""// With Singleton - single shared logger instance
void handleRequest() {
    Logger::getInstance().log("Request received");
}

void processResponse() {
    Logger::getInstance().log("Response sent");
}
// All logs go to the same place"""


def demonstrate() -> dict:
    """Execute the Singleton pattern demonstration.

    Returns:
        Dictionary containing demonstration output data.
    """
    return {
        "cpp_code": CPP_CODE,
        "before_code": BEFORE_CODE,
        "after_code": AFTER_CODE,
        "intent": (
            "Ensures a class has only one instance and provides a global point "
            "of access to it."
        ),
        "context": (
            "Logging service - ensuring only one logger instance exists throughout "
            "the application lifecycle to prevent resource contention."
        ),
        "pros": [
            "Controlled access to the sole instance",
            "Reduced memory footprint from a single instance",
            "Lazy initialization - instance created only when needed",
        ],
        "cons": [
            "Global state can make testing harder",
            "Violates Single Responsibility Principle in some cases",
            "Can mask bad design (tight coupling)",
        ],
        "anti_pattern": (
            "God Object: Avoid creating a singleton that manages too many unrelated "
            "responsibilities. A singleton should focus on one concern. Also avoid "
            "overusing singletons - they are not a substitute for proper dependency "
            "injection."
        ),
        "uml_diagram": """
┌─────────────────────────┐
│       Logger            │
├─────────────────────────┤
│ -instance: Logger*      │
├─────────────────────────┤
│ -Logger()               │
│ +getInstance(): Logger& │
│ +log(message: string)   │
└─────────────────────────┘
         ▲
         │ (returns same instance)
    ┌────┴────┐
    │ Client 1│
    │ Client 2│
    └─────────┘""",
    }
