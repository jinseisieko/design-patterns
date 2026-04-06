"""Flyweight Pattern Demonstration (C++).

Real-world context: Word processor rendering thousands of characters - sharing
intrinsic state (glyph data) while keeping extrinsic state (position) separate.

Anti-pattern warning: Premature optimization - Using flyweight for objects that
don't consume significant memory, adding unnecessary complexity.
"""

CPP_CODE = r"""#include <iostream>
#include <unordered_map>
#include <memory>
#include <string>
#include <vector>

// Flyweight: Glyph
class Glyph {
private:
    char character;
    std::string vectorData; // Intrinsic state

public:
    explicit Glyph(char c) : character(c) {
        vectorData = "VectorData('" + std::string(1, c) + "')";
        std::cout << "Created glyph for '" << c << "'\n";
    }
    
    void render(int x, int y) const {
        std::cout << "Rendered '" << character << "' at (" 
                  << x << "," << y << ") using " << vectorData << "\n";
    }
    
    char getCharacter() const { return character; }
};

// Flyweight Factory
class GlyphFactory {
private:
    std::unordered_map<char, std::unique_ptr<Glyph>> cache;

public:
    const Glyph* getGlyph(char c) {
        if (cache.find(c) == cache.end()) {
            cache[c] = std::make_unique<Glyph>(c);
        }
        return cache[c].get();
    }
    
    size_t getCacheSize() const { return cache.size(); }
};

int main() {
    GlyphFactory factory;
    
    // Document with repeated characters
    std::string text = "Hello World! Hello again!";
    int x = 0;
    
    for (char c : text) {
        const Glyph* glyph = factory.getGlyph(c);
        glyph->render(x, 0);
        x += 10;
    }
    
    std::cout << "\nGlyphs created: " << factory.getCacheSize() 
              << " (not " << text.size() << ")\n";
}"""

BEFORE_CODE = r"""// Without Flyweight - creating glyph for every character
for (char c : document) {
    Glyph* g = new Glyph(c);  // Creates vector data each time
    g->render(x, y);
    delete g;
}
// 'H' appears 2000 times -> 2000 identical objects"""

AFTER_CODE = r"""// With Flyweight - sharing glyphs
GlyphFactory factory;
for (char c : document) {
    const Glyph* g = factory.getGlyph(c);  // Returns shared instance
    g->render(x, y);
}
// 'H' appears 2000 times -> 1 shared glyph object"""


def demonstrate() -> dict:
    """Execute the Flyweight pattern demonstration."""
    return {
        "cpp_code": CPP_CODE,
        "before_code": BEFORE_CODE,
        "after_code": AFTER_CODE,
        "intent": (
            "Minimizes memory usage by sharing as much data as possible with "
            "similar objects. Separates intrinsic (shared) and extrinsic (unique) state."
        ),
        "context": (
            "Word processor rendering thousands of characters - sharing glyph "
            "vector data while keeping positions separate."
        ),
        "pros": [
            "Dramatically reduces memory footprint for many similar objects",
            "Centralizes state that would otherwise be duplicated",
            "Thread-safe if flyweights are immutable",
        ],
        "cons": [
            "Runtime cost of managing shared objects",
            "Complexity of separating intrinsic vs extrinsic state",
            "Not beneficial if few objects exist",
        ],
        "anti_pattern": (
            "Premature Optimization: Don't use Flyweight for objects that don't "
            "consume significant memory. The complexity overhead is only justified "
            "when memory savings are substantial."
        ),
        "uml_diagram": """
┌──────────────────┐
│     Glyph        │  (Flyweight)
├──────────────────┤
│ -character       │  (intrinsic state)
│ -vectorData      │  (intrinsic state, shared)
├──────────────────┤
│ +render(x,y)     │  (extrinsic state passed in)
│ +getCharacter()  │
└──────────────────┘

┌──────────────────┐
│ GlyphFactory     │
├──────────────────┤
│ -cache<char,Glyph│
├──────────────────┤
│ +getGlyph(char)  │──> returns shared Glyph*
│ +getCacheSize()  │
└──────────────────┘""",
    }
