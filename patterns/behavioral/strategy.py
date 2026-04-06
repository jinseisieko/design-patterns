"""Strategy Pattern Demonstration (C++).

Real-world context: Allowing a user to select different sorting algorithms
(e.g., Bubble Sort, Quick Sort) for search results at runtime.

Anti-pattern warning: Premature Optimization - Introducing multiple algorithms
when the built-in std::sort is sufficient and highly optimized.
"""

CPP_CODE = r"""#include <iostream>
#include <vector>
#include <algorithm>
#include <functional>

// Strategy: type alias for a callable
using SortStrategy = std::function<void(std::vector<int>&)>;

// Concrete Strategies
void bubbleSort(std::vector<int>& data) {
    std::cout << "Applying Bubble Sort (O(n^2))...\n";
    for (size_t i = 0; i < data.size(); ++i) {
        for (size_t j = 0; j < data.size() - 1; ++j) {
            if (data[j] > data[j + 1])
                std::swap(data[j], data[j + 1]);
        }
    }
}

void quickSort(std::vector<int>& data) {
    std::cout << "Applying Quick Sort (O(n log n))...\n";
    std::sort(data.begin(), data.end());
}

// Context
class Sorter {
private:
    SortStrategy strategy;
public:
    explicit Sorter(SortStrategy s) : strategy(std::move(s)) {}
    void setStrategy(SortStrategy s) { strategy = std::move(s); }
    void sort(std::vector<int>& data) {
        if (strategy) strategy(data);
    }
};

int main() {
    std::vector<int> data = {64, 34, 25, 12, 22, 11, 90};
    
    Sorter sorter(bubbleSort);
    sorter.sort(data);
    // data is now sorted by bubble sort
    
    sorter.setStrategy(quickSort);
    sorter.sort(data);
    // data is now sorted by quick sort
}"""

BEFORE_CODE = r"""// Without Strategy - hardcoded algorithm
class DataProcessor {
    void sort(vector<int>& data) {
        // Bubble sort hardcoded
        for (int i = 0; i < data.size(); i++)
            for (int j = 0; j < data.size()-1; j++)
                if (data[j] > data[j+1]) swap(data[j], data[j+1]);
    }
    // To change algorithm, must modify this class
}"""

AFTER_CODE = r"""// With Strategy - algorithm selected at runtime
class Sorter {
    SortStrategy strategy;
    void sort(vector<int>& data) { strategy(data); }
};

Sorter sorter(bubbleSort);  // or quickSort, mergeSort, etc.
sorter.sort(data);"""


def demonstrate() -> dict:
    """Execute the Strategy pattern demonstration."""
    return {
        "cpp_code": CPP_CODE,
        "before_code": BEFORE_CODE,
        "after_code": AFTER_CODE,
        "intent": (
            "Defines a family of algorithms, encapsulates each one, and makes them "
            "interchangeable. Lets the algorithm vary independently from clients."
        ),
        "context": (
            "Search result sorting - allowing users to select different sorting "
            "algorithms (Bubble Sort, Quick Sort) from a dropdown at runtime."
        ),
        "pros": [
            "Algorithms can be changed at runtime",
            "Eliminates conditional statements for algorithm selection",
            "Open-Closed: add new strategies without modifying context",
        ],
        "cons": [
            "Clients must understand different strategies to choose the right one",
            "Overhead of additional objects",
        ],
        "anti_pattern": (
            "Premature Optimization: Python's built-in sorted() uses Timsort which "
            "is highly optimized. Only implement custom strategies when you need "
            "specific algorithmic properties or for educational purposes."
        ),
        "uml_diagram": """
┌─────────────────┐         ┌─────────────────┐
│     Sorter      │────────>│  SortStrategy   │
│   (Context)     │         │  (interface)    │
├─────────────────┤         ├─────────────────┤
│ -strategy       │         └────────┬────────
├─────────────────           ┌──────┼──────┐
│ +sort(data)     │           ▼             ▼
│ +setStrategy()  │    ┌──────────┐ ┌──────────┐
└─────────────────┘    │BubbleSort│ │QuickSort │
                       └──────────┘ └──────────┘""",
    }
