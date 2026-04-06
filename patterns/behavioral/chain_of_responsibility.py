"""Chain of Responsibility Pattern Demonstration (C++).

Real-world context: Multi-level logging system - passing log requests along a
chain of handlers where each decides whether to process or pass to next.

Anti-pattern warning: Unhandled requests - Requests reaching end of chain
silently, causing hard-to-debug issues.
"""

CPP_CODE = r"""#include <iostream>
#include <memory>
#include <string>

// Handler Interface
class Logger {
protected:
    std::unique_ptr<Logger> successor;
public:
    virtual ~Logger() = default;
    void setSuccessor(std::unique_ptr<Logger> next) {
        successor = std::move(next);
    }
    Logger* getSuccessor() { return successor.get(); }
    
    void handleLog(int level, const std::string& msg) {
        if (canHandle(level)) {
            log(level, msg);
        }
        if (successor) {
            successor->handleLog(level, msg);
        }
    }
protected:
    virtual bool canHandle(int level) const = 0;
    virtual void log(int level, const std::string& msg) = 0;
};

// Concrete Handlers
class ConsoleLogger : public Logger {
protected:
    bool canHandle(int level) const override { return level == 1; }
    void log(int, const std::string& msg) override {
        std::cout << "CONSOLE [HIGH]: " << msg << "\n";
    }
};

class FileLogger : public Logger {
protected:
    bool canHandle(int level) const override { return level == 2; }
    void log(int, const std::string& msg) override {
        std::cout << "FILE [MEDIUM]: " << msg << "\n";
    }
};

class NetworkLogger : public Logger {
protected:
    bool canHandle(int level) const override { return level == 3; }
    void log(int, const std::string& msg) override {
        std::cout << "NETWORK [LOW]: " << msg << "\n";
    }
};

int main() {
    auto console = std::make_unique<ConsoleLogger>();
    auto file = std::make_unique<FileLogger>();
    auto network = std::make_unique<NetworkLogger>();

    console->setSuccessor(std::move(file));
    console->getSuccessor()->setSuccessor(std::move(network));

    console->handleLog(1, "Critical error!");
    console->handleLog(2, "Warning message");
    console->handleLog(3, "Debug info");
    console->handleLog(4, "Unknown level");
}"""

BEFORE_CODE = r"""// Without Chain - hardcoded routing logic
void log(int level, const string& msg) {
    if (level == 1) {
        console->log(msg);
    } else if (level == 2) {
        file->log(msg);
    } else if (level == 3) {
        network->log(msg);
    }
    // Hard to extend with new loggers
}"""

AFTER_CODE = r"""// With Chain - flexible handler chain
void log(int level, const string& msg) {
    chain->handleLog(level, msg);
    // Easy to add/remove loggers from chain
}"""


def demonstrate() -> dict:
    """Execute the Chain of Responsibility pattern demonstration."""
    return {
        "cpp_code": CPP_CODE,
        "before_code": BEFORE_CODE,
        "after_code": AFTER_CODE,
        "intent": (
            "Allows a request to be passed along a chain of handlers. Each handler "
            "decides whether to process the request or pass it to the next handler."
        ),
        "context": (
            "Multi-level logging system - log messages pass through ConsoleLogger, "
            "FileLogger, NetworkLogger chain."
        ),
        "pros": [
            "Decouples sender from receiver",
            "Easy to add/remove handlers dynamically",
            "Single Responsibility: each handler focuses on one concern",
        ],
        "cons": [
            "Request may go unhandled if chain is misconfigured",
            "Hard to debug - no guarantee which handler will process",
            "Performance overhead of passing through chain",
        ],
        "anti_pattern": (
            "Unhandled Requests: Always provide a default handler at the end of "
            "the chain to catch unprocessed requests, or throw an exception. "
            "Silently dropped requests cause hard-to-debug issues."
        ),
        "uml_diagram": """
┌─────────────────┐
│    Logger       │
├─────────────────┤
│ -successor      │
├─────────────────┤
│ +setSuccessor() │
│ +handleLog()    │
└────────┬────────┘
         │ (chain)
    ┌────┼────────────────┐
    ▼    ▼                ▼
┌────────┐ ┌────────┐ ┌────────┐
│Console │─>│ File   │─>│Network │
│Logger  │  │ Logger │  │ Logger │
└────────┘ └────────┘ └────────┘""",
    }
