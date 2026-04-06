"""Proxy Pattern Demonstration (C++).

Real-world context: Lazy-loading large images in a gallery application -
the proxy holds a reference to the file path and only loads image data when displayed.

Anti-pattern warning: Unnecessary Indirection - Using a proxy for objects that
are already fast and cheap to create.
"""

CPP_CODE = r"""#include <iostream>
#include <memory>
#include <string>

// Subject Interface
class Image {
public:
    virtual void display() = 0;
    virtual ~Image() = default;
};

// RealSubject
class RealImage : public Image {
private:
    std::string fileName;
public:
    explicit RealImage(const std::string& fn) : fileName(fn) {
        std::cout << "Loading image from disk: " << fileName << "\n";
    }
    void display() override {
        std::cout << "Displaying " << fileName << "\n";
    }
};

// Proxy
class ImageProxy : public Image {
private:
    std::string fileName;
    mutable std::unique_ptr<RealImage> realImage;
public:
    explicit ImageProxy(const std::string& fn) : fileName(fn) {}
    
    void display() override {
        if (!realImage) {
            std::cout << "Proxy: Loading image on first access...\n";
            realImage = std::make_unique<RealImage>(fileName);
        }
        realImage->display();
    }
};

int main() {
    std::unique_ptr<Image> img1 = std::make_unique<ImageProxy>("photo1.jpg");
    std::unique_ptr<Image> img2 = std::make_unique<ImageProxy>("photo2.jpg");

    std::cout << "Images created. No loading yet.\n\n";
    
    std::cout << "Displaying img1:\n";
    img1->display();  // Loads here
    
    std::cout << "\nDisplaying img1 again:\n";
    img1->display();  // Already loaded
    
    std::cout << "\nDisplaying img2:\n";
    img2->display();  // Loads here
}"""

BEFORE_CODE = r"""// Without Proxy - loads immediately on creation
class Image {
    Image(string path) {
        data = loadFromDisk(path);  // Expensive!
    }
};

vector<Image> images;
for (auto& path : paths) {
    images.push_back(Image(path));
}
// ALL images loaded at once, even if never displayed"""

AFTER_CODE = r"""// With Proxy - lazy loading on demand
class ImageProxy : public Image {
    void display() {
        if (!realImage) realImage = load(path);
        realImage->display();
    }
};
// Only displayed images are loaded"""


def demonstrate() -> dict:
    """Execute the Proxy pattern demonstration."""
    return {
        "cpp_code": CPP_CODE,
        "before_code": BEFORE_CODE,
        "after_code": AFTER_CODE,
        "intent": (
            "Provides a surrogate or placeholder for another object to control "
            "access to it, commonly used for lazy loading and access control."
        ),
        "context": (
            "Image gallery - lazy-loading large images. The proxy holds the file "
            "path and only loads image data from disk when display() is first called."
        ),
        "pros": [
            "Defers expensive initialization until actually needed",
            "Can add access control or caching transparently",
            "Client code unchanged - proxy implements same interface",
        ],
        "cons": [
            "Adds an extra layer of indirection",
            "Can hide performance issues from developers",
        ],
        "anti_pattern": (
            "Unnecessary Indirection: Don't use a proxy for objects that are "
            "already fast and cheap to create. The proxy pattern is only useful "
            "when the real subject has significant cost to create or access."
        ),
        "uml_diagram": """
┌─────────────────┐
│     Image       │
├─────────────────┤
│ +display()      │
└────────┬────────┘
         │
    ┌────┴───────────┐
    ▼                ▼
┌──────────┐  ┌──────────┐
│RealImage │  │ImageProxy│
├──────────  ├──────────┤
│-fileName │  │-fileName │
│-data     │  │-realImage│
│          │  ├──────────┤
│          │  │+display()│
└──────────┘  │ (lazy)   │
              └──────────┘""",
    }
