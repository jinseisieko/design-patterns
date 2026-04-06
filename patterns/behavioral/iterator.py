"""Iterator Pattern Demonstration (C++).

Real-world context: Custom container traversal - accessing elements of an
aggregate object sequentially without exposing its underlying representation.

Anti-pattern warning: Exposing internal representation - Iterator that leaks
container implementation details, defeating the pattern's purpose.
"""

CPP_CODE = r"""#include <iostream>
#include <vector>
#include <memory>

// Aggregate (Container)
class NumberCollection {
private:
    std::vector<int> numbers;
public:
    explicit NumberCollection(std::initializer_list<int> list) 
        : numbers(list) {}
    
    // Iterator class
    class Iterator {
    private:
        std::vector<int>::iterator current;
        std::vector<int>::iterator endIter;
    public:
        Iterator(std::vector<int>::iterator start, std::vector<int>::iterator end)
            : current(start), endIter(end) {}
        
        void operator++() { if (current != endIter) ++current; }
        bool operator!=(const Iterator& other) const { return current != other.current; }
        int operator*() const { return *current; }
    };
    
    Iterator begin() { return Iterator(numbers.begin(), numbers.end()); }
    Iterator end() { return Iterator(numbers.end(), numbers.end()); }
};

int main() {
    NumberCollection collection({1, 2, 3, 4, 5});
    
    std::cout << "Iterating: ";
    for (auto it = collection.begin(); it != collection.end(); ++it) {
        std::cout << *it << " ";
    }
    std::cout << "\n";
}"""

BEFORE_CODE = r"""// Without Iterator - exposing internal representation
class NumberCollection {
public:
    std::vector<int>& getNumbers() { return numbers; }
    // Client depends on vector implementation
};

for (int i = 0; i < collection.getNumbers().size(); i++) {
    cout << collection.getNumbers()[i];
}"""

AFTER_CODE = r"""// With Iterator - uniform traversal interface
for (auto it = collection.begin(); it != collection.end(); ++it) {
    cout << *it;
}
// Client doesn't know about internal storage"""


def demonstrate() -> dict:
    """Execute the Iterator pattern demonstration."""
    return {
        "cpp_code": CPP_CODE,
        "before_code": BEFORE_CODE,
        "after_code": AFTER_CODE,
        "intent": (
            "Provides a way to access elements of an aggregate object sequentially "
            "without exposing its underlying representation."
        ),
        "context": (
            "Custom container traversal - implementing iterators that work with "
            "range-based for loops and STL algorithms."
        ),
        "pros": [
            "Supports multiple traversals of same collection",
            "Simplifies aggregate interface",
            "Decouples algorithms from container implementation",
        ],
        "cons": [
            "Overkill for simple collections",
            "Can be error-prone if collection changes during iteration",
        ],
        "anti_pattern": (
            "Exposing Internal Representation: Don't let the iterator expose "
            "container internals. The iterator should only provide traversal, "
            "not access to the underlying data structure."
        ),
        "uml_diagram": """
┌──────────────────────┐     ┌──────────────────┐
│ NumberCollection     │     │   Iterator       │
├──────────────────────┤     ├──────────────────┤
│ -numbers: vector     │────>│ +operator++()    │
├──────────────────────┤     │ +operator!=()    │
│ +begin(): Iterator   │     │ +operator*()     │
│ +end(): Iterator     │     └──────────────────┘
└──────────────────────┘""",
    }
