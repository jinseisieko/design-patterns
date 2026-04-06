"""Decorator Pattern Demonstration (C++).

Real-world context: Adding encryption and compression to a data source
dynamically without modifying the base class.

Anti-pattern warning: Performance Degradation - Stacking too many decorators
that perform expensive operations on every call.
"""

CPP_CODE = r"""#include <iostream>
#include <memory>
#include <string>

// Component Interface
class DataSource {
public:
    virtual void writeData(const std::string& data) = 0;
    virtual std::string readData() = 0;
    virtual ~DataSource() = default;
};

// Concrete Component
class FileDataSource : public DataSource {
private:
    std::string filename;
    std::string data;
public:
    explicit FileDataSource(const std::string& fn) : filename(fn) {}
    void writeData(const std::string& d) override {
        data = d;
        std::cout << "Writing to " << filename << "\n";
    }
    std::string readData() override { return data; }
};

// Decorator Base
class DataSourceDecorator : public DataSource {
protected:
    std::unique_ptr<DataSource> source;
public:
    explicit DataSourceDecorator(std::unique_ptr<DataSource> s)
        : source(std::move(s)) {}
    void writeData(const std::string& d) override { source->writeData(d); }
    std::string readData() override { return source->readData(); }
};

// Encryption Decorator
class EncryptionDecorator : public DataSourceDecorator {
public:
    using DataSourceDecorator::DataSourceDecorator;
    void writeData(const std::string& d) override {
        std::string encrypted = "ENC[" + d + "]";
        std::cout << "Encrypting data...\n";
        DataSourceDecorator::writeData(encrypted);
    }
    std::string readData() override {
        std::string d = DataSourceDecorator::readData();
        if (d.find("ENC[") == 0) {
            d = d.substr(4, d.size() - 5);
            std::cout << "Decrypting data...\n";
        }
        return d;
    }
};

// Compression Decorator
class CompressionDecorator : public DataSourceDecorator {
public:
    using DataSourceDecorator::DataSourceDecorator;
    void writeData(const std::string& d) override {
        std::string compressed = "CMP[" + d + "]";
        std::cout << "Compressing data...\n";
        DataSourceDecorator::writeData(compressed);
    }
};

int main() {
    auto file = std::make_unique<FileDataSource>("data.dat");
    
    // Stack decorators: Compression -> Encryption -> File
    auto decorated = std::make_unique<CompressionDecorator>(
        std::make_unique<EncryptionDecorator>(std::move(file))
    );
    
    decorated->writeData("Hello, World!");
    std::string result = decorated->readData();
    std::cout << "Read: " << result << "\n";
}"""

BEFORE_CODE = r"""// Without Decorator - behavior hardcoded in class
class EncryptedFileDataSource {
    void write(string data) {
        // encryption logic mixed with file I/O
    }
};

class CompressedEncryptedFileDataSource {
    // Combinatorial explosion of subclasses
};"""

AFTER_CODE = r"""// With Decorator - compose behaviors at runtime
auto source = make_unique<FileDataSource>("data.dat");
auto encrypted = make_unique<Encryption>(move(source));
auto compressed = make_unique<Compression>(move(encrypted));
// Any combination without class explosion"""


def demonstrate() -> dict:
    """Execute the Decorator pattern demonstration."""
    return {
        "cpp_code": CPP_CODE,
        "before_code": BEFORE_CODE,
        "after_code": AFTER_CODE,
        "intent": (
            "Attaches additional responsibilities to an object dynamically. "
            "Provides a flexible alternative to subclassing for extending functionality."
        ),
        "context": (
            "Data source with optional encryption and compression - stacking "
            "behaviors on a file data source at runtime."
        ),
        "pros": [
            "Add/remove responsibilities at runtime",
            "Avoids combinatorial explosion of subclasses",
            "Open-Closed: extend without modifying existing code",
        ],
        "cons": [
            "Many small decorator classes can be hard to navigate",
            "Stacking many decorators impacts performance",
        ],
        "anti_pattern": (
            "Performance Degradation: Avoid stacking too many decorators that each "
            "perform expensive operations (I/O, computation) on every call. Profile "
            "before adding layers of wrapping."
        ),
        "uml_diagram": """
┌─────────────────┐
│  DataSource     │
├─────────────────┤
│ +writeData()    │
│ +readData()     │
└────────────────┘
         ▲
    ┌────┼────────────────┐
    ▼    ▼                ▼
┌────────┐ ┌────────────┐ ┌────────────┐
│FileData│ │Encryption  │ │Compression │
│ Source │ │ Decorator  │ │ Decorator  │
└────────┘ ├────────────┤ ├────────────┤
           │ -source    │ │ -source    │
           └────────────┘ └────────────┘
                │              │
                └──────┬───────┘
                       ▼
              ┌────────────────
              │   DataSource   │ (wrapped)
              └────────────────┘""",
    }
