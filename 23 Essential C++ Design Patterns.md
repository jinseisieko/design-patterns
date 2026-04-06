# From Theory to Practice: Applying 23 Essential C++ Design Patterns in Game Engines, Networking, and UI Frameworks

## Creational Patterns in Practice

Creational design patterns are concerned with the mechanisms of object creation, aiming to make systems independent of the objects they create and how they are created [[8]]. They promote flexibility by decoupling clients from the concrete classes that produce objects. This section provides deep descriptions and practical C++ examples for five key creational patterns: Abstract Factory, Singleton, Factory Method, Builder, and Prototype. Each example is grounded in a real-world context, such as building cross-platform graphical user interfaces, managing system-wide resources, constructing complex API requests, and cloning expensive game entities.

The **Abstract Factory Pattern** provides an interface for creating families of related or dependent objects without specifying their concrete classes [[42,173]]. Its primary motivation is to encapsulate a group of individual factories with a common theme, ensuring that the resulting objects are compatible with each other. A classic real-world use case is developing a GUI toolkit that must render widgets consistently across different operating systems like Windows, macOS, and Linux. In this scenario, an `AbstractGUIFactory` could declare methods like `createButton()` and `createTextField()`. Platform-specific concrete factories, such as `WindowsGUIFactory` and `LinuxGUIFactory`, would implement these methods to return widgets with the correct native look and feel [[165]]. Using Qt, one could design a factory that produces buttons and scrollbars adhering to either the Fusion style or the system's native style, ensuring visual consistency within the application [[172]]. This prevents client code from being littered with platform-specific instantiation logic, making the application easier to maintain and extend for new platforms.

```cpp
#include <iostream>
#include <memory>

// Abstract Product: Button
class Button {
public:
    virtual void render() = 0;
    virtual ~Button() = default;
};

// Abstract Product: TextField
class TextField {
public:
    virtual void addText(const std::string& text) = 0;
    virtual ~TextField() = default;
};

// Concrete Product: WindowsButton
class WindowsButton : public Button {
public:
    void render() override {
        std::cout << "Rendering a native Windows button.\n";
    }
};

// Concrete Product: WindowsTextField
class WindowsTextField : public TextField {
public:
    void addText(const std::string& text) override {
        std::cout << "Adding text '" << text << "' to a Windows text field.\n";
    }
};

// Concrete Product: MacButton
class MacButton : public Button {
public:
    void render() override {
        std::cout << "Rendering a native Mac button.\n";
    }
};

// Concrete Product: MacTextField
class MacTextField : public TextField {
public:
    void addText(const std::string& text) override {
        std::cout << "Adding text '" << text << "' to a Mac text field.\n";
    }
};

// Abstract Factory
class GUIFactory {
public:
    virtual std::unique_ptr<Button> createButton() = 0;
    virtual std::unique_ptr<TextField> createTextField() = 0;
    virtual ~GUIFactory() = default;
};

// Concrete Factory: Windows Factory
class WindowsGUIFactory : public GUIFactory {
public:
    std::unique_ptr<Button> createButton() override {
        return std::make_unique<WindowsButton>();
    }
    std::unique_ptr<TextField> createTextField() override {
        return std::make_unique<WindowsTextField>();
    }
};

// Concrete Factory: Mac Factory
class MacGUIFactory : public GUIFactory {
public:
    std::unique_ptr<Button> createButton() override {
        return std::make_unique<MacButton>();
    }
    std::unique_ptr<TextField> createTextField() override {
        return std::make_unique<MacTextField>();
    }
};

// Client Code
void clientCode(std::unique_ptr<GUIFactory> factory) {
    auto button = factory->createButton();
    auto textField = factory->createTextField();
    button->render();
    textField->addText("Hello, World!");
}
```

The **Singleton Pattern** ensures a class has only one instance and provides a global point of access to it [[73,154]]. It is ideal for managing shared resources like configuration managers, connection pools, or loggers, where having multiple instances would lead to resource contention or inconsistent state . A critical aspect of implementing Singletons in modern C++ is thread safety. Since C++11, a simple and elegant solution involves defining a local static variable inside a function, which guarantees thread-safe initialization [[149,455,456]]. However, a significant anti-pattern is overusing Singletons to manage unrelated responsibilities, turning them into "God Objects" that violate the Single Responsibility Principle [[73]]. While some frameworks like Qt have single-instance objects like `QGuiApplication` [[229]], care must be taken as improper management can lead to errors if a second instance is attempted [[381]].

```cpp
#include <iostream>
#include <mutex>

// Logger Singleton
class Logger {
private:
    // Private constructor prevents instantiation
    Logger() { 
        std::cout << "Logger instance created.\n"; 
    }

    // Static mutex for thread safety (though C++11+ local statics are safer)
    static std::mutex instance_mutex_;

public:
    // Deleted copy constructor and assignment operator prevent copying
    Logger(const Logger&) = delete;
    Logger& operator=(const Logger&) = delete;

    // Static method to provide global access point
    static Logger& getInstance() {
        // Local static variable is guaranteed to be thread-safe since C++11
        static Logger instance;
        return instance;
    }

    void log(const std::string& message) {
        std::cout << "[LOG] " << message << "\n";
    }
};

// Define the static mutex (needed for older C++ standards)
std::mutex Logger::instance_mutex_;

// Example usage
void demonstrateSingleton() {
    Logger& logger1 = Logger::getInstance();
    Logger& logger2 = Logger::getInstance();

    logger1.log("This is a log message.");
    // Both references point to the same instance
    if (&logger1 == &logger2) {
        std::cout << "logger1 and logger2 are the same instance.\n";
    }
}
```

The **Factory Method Pattern** is a creational pattern that lets a class delegate the responsibility of instantiating itself to its subclasses [[9]]. This is useful when a system should be independent of how its products are created. Instead of calling a constructor directly, a client calls a factory method, which returns an object of a product class. Subclasses can then override this method to change the class of the object that will be instantiated [[10]]. A practical example in a high-performance networking library like Boost.Asio involves creating different types of asynchronous handlers based on the type of I/O operation (e.g., a TCP socket handler vs. a timer handler) [[240]]. Another example is in a web server framework where a base `RequestHandler` class defines a factory method `createResponse()`. Different HTTP method handlers, like `GetHandler` and `PostHandler`, can override this method to return their specific response formats, centralizing the creation logic while allowing for specialization [[466]]. The implementation within Qt often involves static factory methods on classes, avoiding the need for a separate factory object [[275]].

```cpp
#include <iostream>
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

// Example usage
void demonstrateFactoryMethod() {
    std::unique_ptr<PaymentGateway> gateway;

    // Using a credit card gateway
    gateway = std::make_unique<CreditCardGateway>();
    gateway->executePayment(100.50); // Output: Processing $100.5 via Credit Card.

    // Switching to a PayPal gateway
    gateway = std::make_unique<PayPalGateway>();
    gateway->executePayment(250.75); // Output: Processing $250.75 via PayPal.
}
```

The **Builder Pattern** separates the construction of a complex object from its representation, allowing the same construction process to create various representations [[192]]. It is particularly useful when an object needs a large number of optional parameters or when its construction algorithm should be independent of the parts that compose it. A prime real-world example is constructing sophisticated HTTP requests in a C++ networking library like Boost.Beast [[433]]. An HTTP request might require a URL, headers, a body, authentication credentials, timeouts, and proxy settings. A Builder class allows these components to be set step-by-step, improving readability and reducing the cognitive load compared to a long constructor with many arguments [[304]]. This approach makes the code more robust and less prone to errors from incorrect parameter ordering. The fluent interface, where each setter returns a reference to the builder itself, enables a clean, chained syntax (`requestBuilder.setUrl(...).addHeader(...).build()`).

```cpp
#include <iostream>
#include <string>
#include <map>

// Product: HTTP Request
class HttpRequest {
private:
    std::string url;
    std::map<std::string, std::string> headers;
    std::string body;
    std::string method;

public:
    void setUrl(const std::string& u) { url = u; }
    void addHeader(const std::string& key, const std::string& value) { headers[key] = value; }
    void setBody(const std::string& b) { body = b; }
    void setMethod(const std::string& m) { method = m; }

    void display() const {
        std::cout << "=== HTTP Request ===\n";
        std::cout << "Method: " << method << " " << url << "\n";
        std::cout << "Headers:\n";
        for (const auto& [key, value] : headers) {
            std::cout << "  " << key << ": " << value << "\n";
        }
        if (!body.empty()) {
            std::cout << "Body: " << body << "\n";
        }
        std::cout << "==================\n\n";
    }
};

// Builder
class HttpRequestBuilder {
private:
    HttpRequest request;

public:
    HttpRequestBuilder& setUrl(const std::string& url) {
        request.setUrl(url);
        return *this;
    }
    
    HttpRequestBuilder& addHeader(const std::string& key, const std::string& value) {
        request.addHeader(key, value);
        return *this;
    }
    
    HttpRequestBuilder& setBody(const std::string& body) {
        request.setBody(body);
        return *this;
    }
    
    HttpRequestBuilder& setMethod(const std::string& method) {
        request.setMethod(method);
        return *this;
    }
    
    HttpRequest build() {
        return std::move(request);
    }
};

// Example usage
void demonstrateBuilder() {
    HttpRequest postRequest = HttpRequestBuilder{}
        .setUrl("/api/users")
        .addHeader("Content-Type", "application/json")
        .addHeader("Authorization", "Bearer token123")
        .setMethod("POST")
        .setBody(R"({"name": "John Doe", "email": "john@example.com"})")
        .build();

    postRequest.display();

    HttpRequest getRequest = HttpRequestBuilder{}
        .setUrl("/api/users/123")
        .addHeader("Accept", "application/json")
        .setMethod("GET")
        .build();

    getRequest.display();
}
```

The **Prototype Pattern** is a creational design pattern that allows you to copy existing objects without making your code dependent on their classes [[23]]. It is most effective when object creation is expensive, such as initializing a heavy database connection or loading a large model file. Instead of creating a new instance from scratch, a prototype object is cloned [[22]]. A quintessential example is in game development, where spawning hundreds of similar enemy units by cloning a pre-configured "prototype" enemy is vastly more efficient than instantiating each one individually from its class constructor [[20,177]]. Modern C++ supports polymorphic cloning through a pure virtual `clone()` method in an abstract base class. The derived classes implement this method to return a new instance of their own type, correctly copying all member data [[55]]. This technique, sometimes called the Virtual Constructor Idiom, is essential for safely creating copies of objects through a base-class pointer [[54,322]].

```cpp
#include <iostream>
#include <memory>
#include <vector>

// Abstract Prototype
class Unit {
public:
    virtual ~Unit() = default;
    virtual std::unique_ptr<Unit> clone() const = 0;
    virtual void display() const = 0;
};

// Concrete Prototype: Archer
class Archer : public Unit {
private:
    int health;
    int damage;

public:
    Archer(int h = 100, int d = 20) : health(h), damage(d) {}
    
    std::unique_ptr<Unit> clone() const override {
        return std::make_unique<Archer>(*this); // Copy constructor
    }
    
    void display() const override {
        std::cout << "An archer with " << health << " health and " << damage << " damage.\n";
    }
};

// Concrete Prototype: Knight
class Knight : public Unit {
private:
    int health;
    int damage;
    bool isMounted;

public:
    Knight(int h = 150, int d = 30, bool mounted = true) 
        : health(h), damage(d), isMounted(mounted) {}
    
    std::unique_ptr<Unit> clone() const override {
        return std::make_unique<Knight>(*this);
    }
    
    void display() const override {
        std::cout << "A knight with " << health << " health, " << damage 
                  << " damage, and " << (isMounted ? "mounted" : "on foot") << ".\n";
    }
};

// Prototype Manager / Cloning Client
class UnitFactory {
private:
    std::vector<std::unique_ptr<Unit>> prototypes;

public:
    UnitFactory() {
        // Initialize with prototype configurations
        prototypes.push_back(std::make_unique<Archer>());
        prototypes.push_back(std::make_unique<Knight>());
    }
    
    std::unique_ptr<Unit> createUnit(int prototypeIndex) {
        if (prototypeIndex >= 0 && prototypeIndex < prototypes.size()) {
            return prototypes[prototypeIndex]->clone();
        }
        return nullptr;
    }
};

// Example usage
void demonstratePrototype() {
    UnitFactory factory;
    
    auto archer1 = factory.createUnit(0);
    auto knight1 = factory.createUnit(1);
    auto archer2 = factory.createUnit(0); // Clone another archer
    
    std::cout << "Created units:\n";
    archer1->display(); // An archer with 100 health and 20 damage.
    knight1->display(); // A knight with 150 health, 30 damage, and mounted.
    archer2->display(); // An archer with 100 health and 20 damage.
}
```

## Structural Patterns for System Architecture

Structural design patterns focus on how classes and objects are composed to form larger structures. They provide ways to compose classes or objects to realize new functionality while keeping the system flexible and reusable [[299]]. These patterns are crucial for designing robust and scalable systems, particularly in domains like game development and high-performance computing where complex interactions between components are the norm. This section explores seven structural patterns—Adapter, Bridge, Composite, Decorator, Facade, Flyweight, and Proxy—with practical C++ examples drawn from real-world contexts such as integrating legacy systems, decoupling abstractions from implementations, rendering graphical scenes, and controlling access to remote resources.

The **Adapter Pattern** acts as a bridge between two incompatible interfaces, allowing classes with incompatible interfaces to work together [[204]]. This is invaluable when integrating third-party libraries or legacy code into a new system. For example, consider a modern graphics engine that needs to support an old payment gateway library. The adapter would wrap the old library's interface and translate its methods into calls that conform to the engine's new payment processing interface [[49,205]]. This avoids rewriting the entire legacy component. A common implementation is the Object Adapter, where the adapter holds a reference to the adaptee object and delegates calls to it [[205]]. In C++, this can be achieved by inheriting publicly from the target interface and privately from the adaptee class, or by composition, where the adapter contains a private member of the adaptee's type. The latter is often preferred as it promotes loose coupling [[47]].

```cpp
#include <iostream>
#include <string>

// Target Interface
class MediaPlayer {
public:
    virtual void play(const std::string& audioType, const std::string& fileName) = 0;
    virtual ~MediaPlayer() = default;
};

// Adaptee: Legacy Advanced Media Player
class AdvancedMediaPlayer {
public:
    virtual void playVlc(const std::string& fileName) = 0;
    virtual void playMp4(const std::string& fileName) = 0;
};

// Concrete Adaptee
class VlcPlayer : public AdvancedMediaPlayer {
public:
    void playVlc(const std::string& fileName) override {
        std::cout << "Playing VLC file. Name: " << fileName << "\n";
    }
    void playMp4(const std::string& fileName) override {
        // Do nothing for MP4
    }
};

class Mp4Player : public AdvancedMediaPlayer {
public:
    void playVlc(const std::string& fileName) override {
        // Do nothing for VLC
    }
    void playMp4(const std::string& fileName) override {
        std::cout << "Playing MP4 file. Name: " << fileName << "\n";
    }
};

// Adapter
class MediaAdapter : public MediaPlayer {
private:
    std::unique_ptr<AdvancedMediaPlayer> advancedMusicPlayer;

public:
    MediaAdapter(const std::string& audioType) {
        if (audioType == "vlc") {
            advancedMusicPlayer = std::make_unique<VlcPlayer>();
        } else if (audioType == "mp4") {
            advancedMusicPlayer = std::make_unique<Mp4Player>();
        }
    }

    void play(const std::string& audioType, const std::string& fileName) override {
        if (advancedMusicPlayer) {
            if (audioType == "vlc") {
                advancedMusicPlayer->playVlc(fileName);
            } else if (audioType == "mp4") {
                advancedMusicPlayer->playMp4(fileName);
            }
        } else {
            std::cout << "Invalid media. " << audioType << " format not supported.\n";
        }
    }
};

// Concrete Target
class AudioPlayer : public MediaPlayer {
private:
    std::unique_ptr<MediaAdapter> mediaAdapter;

public:
    void play(const std::string& audioType, const std::string& fileName) override {
        // Native support for mp3 files
        if (audioType == "mp3") {
            std::cout << "Playing mp3 file. Name: " << fileName << "\n";
        }
        // Check if it can be played via adapter
        else if (audioType == "vlc" || audioType == "mp4") {
            mediaAdapter = std::make_unique<MediaAdapter>(audioType);
            mediaAdapter->play(audioType, fileName);
        } else {
            std::cout << "Invalid media. " << audioType << " format not supported.\n";
        }
    }
};

// Example usage
void demonstrateAdapter() {
    AudioPlayer player;
    player.play("mp3", "beyond the horizon.mp3");
    player.play("vlc", "far far away.vlc");
    player.play("mp4", "mind me.mp4");
}
```

The **Bridge Pattern** decouples an abstraction from its implementation so that the two can vary independently [[67,68]]. This is powerful for creating highly extensible systems. A classic example is a drawing application. The `Shape` abstraction (e.g., Circle, Rectangle) can exist separately from the `DrawingAPI` implementation (e.g., OpenGL, DirectX, SVG) [[211]]. By using composition instead of inheritance, a `Circle` object can be rendered using any available `DrawingAPI` without modification. This separation allows developers to add new shapes or new rendering backends without recompiling existing code [[224]]. The PIMPL (Pointer to Implementation) idiom in C++ is a common, albeit simpler, application of the Bridge pattern, where a public class hides a pointer to a private implementation class to break compilation dependencies [[221,222]].

```cpp
#include <iostream>

// Implementor Interface
class DrawingAPI {
public:
    virtual void drawCircle(double x, double y, double radius) = 0;
    virtual ~DrawingAPI() = default;
};

// Concrete Implementor: DrawingAPIv1
class DrawingAPIv1 : public DrawingAPI {
public:
    void drawCircle(double x, double y, double radius) override {
        std::cout << "API v1 circle at (" << x << "," << y << ") with radius " << radius << ".\n";
    }
};

// Concrete Implementor: DrawingAPIv2
class DrawingAPIv2 : public DrawingAPI {
public:
    void drawCircle(double x, double y, double radius) override {
        std::cout << "API v2 circle at (" << x << "," << y << ") with radius " << radius << ".\n";
    }
};

// Refined Abstraction
class CircleShape {
protected:
    double x, y, radius;
    std::unique_ptr<DrawingAPI> drawingAPI;

public:
    CircleShape(double x, double y, double radius, std::unique_ptr<DrawingAPI> api)
        : x(x), y(y), radius(radius), drawingAPI(std::move(api)) {}

    virtual void draw() {
        drawingAPI->drawCircle(x, y, radius);
    }
    
    virtual void resize(double factor) {
        radius *= factor;
    }
};

// Concrete Abstraction: SquareShape
class SquareShape : public CircleShape {
public:
    SquareShape(double x, double y, double sideLength, std::unique_ptr<DrawingAPI> api)
        : CircleShape(x, y, sideLength / 2.0, std::move(api)) {} // Treat square as a special circle

    void draw() override {
        std::cout << "Drawing a square at (" << x << "," << y << ") with side length " << radius * 2.0 << ".\n";
        // Delegate the actual drawing to the DrawingAPI
        drawingAPI->drawCircle(x, y, radius);
    }
};

// Example usage
void demonstrateBridge() {
    auto v1api = std::make_unique<DrawingAPIv1>();
    auto v2api = std::make_unique<DrawingAPIv2>();

    CircleShape circle1(1, 2, 3, std::move(v1api));
    SquareShape square1(5, 7, 10, std::move(v2api));

    circle1.draw(); // Uses DrawingAPIv1
    square1.draw(); // Uses DrawingAPIv2
}
```

The **Composite Pattern** allows you to compose objects into tree structures to represent part-whole hierarchies. It lets clients treat individual objects and compositions of objects uniformly [[27]]. This is fundamental in graphical applications, particularly scene graphs. A `SceneNode` can be a composite that contains other `SceneNode`s (children), while a primitive shape like a `Cube` or `Sphere` is a leaf node [[188,214]]. A visitor can traverse the entire graph, performing operations like rendering or collision detection on every node, regardless of whether it's a composite or a leaf [[214]]. This pattern simplifies client code by eliminating the need to differentiate between individual objects and groups of objects. In Qt, the model/view architecture also leverages a similar concept, where item models can represent hierarchical data [[166,500]].

```cpp
#include <iostream>
#include <vector>
#include <memory>

// Component Interface
class Graphic {
public:
    virtual void move(int x, int y) = 0;
    virtual void draw() = 0;
    virtual ~Graphic() = default;
};

// Leaf
class Dot : public Graphic {
private:
    int x, y;
public:
    Dot(int x, int y) : x(x), y(y) {}
    void move(int dx, int dy) override {
        x += dx;
        y += dy;
    }
    void draw() override {
        std::cout << "Drawing dot at (" << x << "," << y << ").\n";
    }
};

// Composite
class CompoundGraphic : public Graphic {
private:
    std::vector<std::unique_ptr<Graphic>> children;
public:
    void add(std::unique_ptr<Graphic> graphic) {
        children.push_back(std::move(graphic));
    }
    
    void move(int dx, int dy) override {
        for (auto& child : children) {
            child->move(dx, dy);
        }
    }
    
    void draw() override {
        std::cout << "Compound Graphic begins:\n";
        for (auto& child : children) {
            child->draw();
        }
        std::cout << "Compound Graphic ends.\n";
    }
};

// Example usage
void demonstrateComposite() {
    auto p1 = std::make_unique<Dot>(1, 2);
    auto p2 = std::make_unique<Dot>(3, 4);
    auto p3 = std::make_unique<Dot>(5, 6);

    auto group = std::make_unique<CompoundGraphic>();
    group->add(std::move(p1));
    group->add(std::move(p2));

    auto rootGroup = std::make_unique<CompoundGraphic>();
    rootGroup->add(std::move(p3));
    rootGroup->add(std::move(group));

    rootGroup->draw();
    // Output shows the nested structure of drawings
}
```

The **Decorator Pattern** attaches additional responsibilities to an object dynamically. It provides a flexible alternative to subclassing for extending functionality [[96]]. Decorators follow the same interface as the objects they wrap, making them transparent to the client. A classic use case is in network programming, where a raw socket object can be wrapped by a series of decorators to add features like encryption, compression, or logging [[81]]. Each decorator implements the `Socket` interface and holds a reference to a `Socket` object, delegating the core operations to it while adding its own behavior before or after. This creates a "onion-like" structure where multiple behaviors can be layered onto a single object. This approach is superior to inheritance because it allows for combinations of behaviors that would be impossible to achieve with a rigid class hierarchy.

```cpp
#include <iostream>
#include <memory>

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
    explicit FileDataSource(const std::string& filename) : filename(filename) {}
    void writeData(const std::string& data) override {
        this->data = data;
        std::cout << "Writing data to file: " << filename << "\n";
    }
    std::string readData() override {
        std::cout << "Reading data from file: " << filename << "\n";
        return data;
    }
};

// Decorator Base
class DataSourceDecorator : public DataSource {
protected:
    std::unique_ptr<DataSource> source;
public:
    explicit DataSourceDecorator(std::unique_ptr<DataSource> source) : source(std::move(source)) {}
    void writeData(const std::string& data) override {
        source->writeData(data);
    }
    std::string readData() override {
        return source->readData();
    }
};

// Concrete Decorator
class EncryptionDecorator : public DataSourceDecorator {
public:
    using DataSourceDecorator::DataSourceDecorator;
    
    void writeData(const std::string& data) override {
        std::string encrypted = "ENCRYPTED:" + data;
        std::cout << "Encrypting data before writing...\n";
        DataSourceDecorator::writeData(encrypted);
    }
    
    std::string readData() override {
        std::string decrypted = DataSourceDecorator::readData();
        if (decrypted.find("ENCRYPTED:") == 0) {
            decrypted = decrypted.substr(8); // Remove "ENCRYPTED:"
            std::cout << "Decrypting data after reading...\n";
        }
        return decrypted;
    }
};

// Concrete Decorator
class CompressionDecorator : public DataSourceDecorator {
public:
    using DataSourceDecorator::DataSourceDecorator;
    
    void writeData(const std::string& data) override {
        std::string compressed = "COMPRESSED:[" + data + "]";
        std::cout << "Compressing data before writing...\n";
        DataSourceDecorator::writeData(compressed);
    }
};

// Example usage
void demonstrateDecorator() {
    auto fileSource = std::make_unique<FileDataSource>("data.dat");
    
    // Wrap the source with decorators
    auto encryptedSource = std::make_unique<EncryptionDecorator>(std::move(fileSource));
    auto compressedEncryptedSource = std::make_unique<CompressionDecorator>(std::move(encryptedSource));
    
    // Use the decorated object
    compressedEncryptedSource->writeData("Hello, World!");
    std::string result = compressedEncryptedSource->readData();
    std::cout << "Read data: " << result << "\n";
}
```

The **Facade Pattern** provides a unified interface to a subsystem of interfaces, making the subsystem easier to use [[101]]. It defines a higher-level interface that shields clients from the complex underlying logic. A compelling example is a `DatabaseManager` facade for a complex database interaction system [[99]]. Instead of exposing low-level APIs for connecting to MySQL, PostgreSQL, or SQLite, executing raw SQL queries, and handling transactions, the facade presents simple, domain-oriented methods like `saveUser(const User& user)` or `findProductById(int id)`. This simplifies the client's task immensely and reduces the risk of misuse. The facade coordinates calls to the various subsystems (e.g., connection pool, query parser, transaction manager) internally, acting as a single point of contact [[99]].

```cpp
#include <iostream>

// Subsystem Classes
class ConnectionPool {
public:
    void init() { std::cout << "Initializing connection pool.\n"; }
    void release() { std::cout << "Releasing connections.\n"; }
};

class QueryParser {
public:
    void parse(const std::string& query) {
        std::cout << "Parsing SQL query: " << query << "\n";
    }
};

class TransactionManager {
public:
    void begin() { std::cout << "Starting transaction.\n"; }
    void commit() { std::cout << "Committing transaction.\n"; }
    void rollback() { std::cout << "Rolling back transaction.\n"; }
};

// Facade
class DatabaseFacade {
private:
    ConnectionPool connectionPool;
    QueryParser queryParser;
    TransactionManager transactionManager;

public:
    void connect() {
        connectionPool.init();
    }
    
    void disconnect() {
        connectionPool.release();
    }
    
    void executeUpdate(const std::string& query) {
        transactionManager.begin();
        try {
            queryParser.parse(query);
            // Simulate update execution
            std::cout << "Executing update on database.\n";
            transactionManager.commit();
        } catch (...) {
            transactionManager.rollback();
            throw;
        }
    }
};

// Example usage
void demonstrateFacade() {
    DatabaseFacade db;
    db.connect();
    db.executeUpdate("INSERT INTO users (name) VALUES ('Alice')");
    db.disconnect();
}
```

The **Flyweight Pattern** is a structural pattern that focuses on minimizing memory usage by sharing as much data as possible with similar objects [[11]]. It is ideal for applications with a large number of fine-grained objects, such as a word processor rendering a document with thousands of characters. The flyweight stores intrinsic state—the part of the object's state that is shared among multiple instances, like character glyphs, font information, or color [[441]]. Extrinsic state—the part that varies per object, like position on the screen—is passed in when the flyweight is used [[13]]. A `Glyph` class might store the vector data for a 'A' character once, but multiple `Glyph` objects can share this single piece of data while having different positions. This dramatically reduces memory consumption. Thread safety is a consideration, as flyweight objects are ideally immutable to prevent race conditions [[12]].

```cpp
#include <iostream>
#include <unordered_map>
#include <memory>
#include <string>

// Flyweight: Glyph
class Glyph {
private:
    char character;
    std::string vectorData; // Intrinsic state: expensive-to-create data

public:
    Glyph(char c) : character(c) {
        // Simulate expensive computation for vector data
        vectorData = "Vector data for character '" + std::string(1, c) + "'";
        std::cout << "Creating vector data for '" << c << "'.\n";
    }
    
    void render(int x, int y) const { // Extrinsic state
        std::cout << "Rendering " << vectorData << " at position (" << x << ", " << y << ")\n";
    }
};

// Flyweight Factory
class GlyphFactory {
private:
    std::unordered_map<char, std::unique_ptr<Glyph>> cache;

public:
    std::unique_ptr<Glyph> getGlyph(char c) {
        if (cache.find(c) == cache.end()) {
            cache[c] = std::make_unique<Glyph>(c);
        }
        return std::unique_ptr<Glyph>(cache[c]->clone()); // Return a copy or a handle
    }
};

// Example usage
void demonstrateFlyweight() {
    GlyphFactory factory;
    std::vector<std::pair<char, std::pair<int, int>>> textLayout = {
        {'H', {0, 0}}, {'e', {10, 0}}, {'l', {20, 0}}, {'l', {30, 0}}, {'o', {40, 0}}
    };

    for (auto& [character, position] : textLayout) {
        auto glyph = factory.getGlyph(character);
        glyph->render(position.first, position.second);
    }
    // Note: This is a simplified example. A production version would likely
    // manage pointers or handles rather than unique_ptrs to avoid recreation.
}
```

The **Proxy Pattern** provides a surrogate or placeholder for another object to control access to it [[74]]. Proxies are used for various reasons, including lazy loading, caching, and controlling access to remote or expensive objects. A common real-world example is lazy-loading a large image in a gallery application [[75]]. A `ImageProxy` object is created immediately, holding the image's file path. The actual image data is loaded from disk only when the `display()` method is first called on the proxy [[76]]. This defers expensive operations until they are truly necessary, improving application startup time. Proxies can also be used to control access to sensitive data, checking permissions before forwarding a request to the real object. Boost.Asio sockets can also be managed through proxies to ensure proper lifecycle and resource cleanup [[397]].

```cpp
#include <iostream>
#include <memory>

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
    explicit RealImage(const std::string& fileName) : fileName(fileName) {
        std::cout << "Loading image from disk: " << fileName << "\n";
        // Simulate slow loading
        for(int i=0; i<1000000; ++i);
        std::cout << "Image " << fileName << " loaded.\n";
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
    mutable bool loading = false;
public:
    explicit ImageProxy(const std::string& fileName) : fileName(fileName) {}
    
    void display() override {
        if (!realImage) {
            // Lazy initialization: create the real object only when needed
            if (!loading) {
                std::cout << "Creating proxy for " << fileName << ". Real object will be created on first access.\n";
                loading = true;
            }
            realImage = std::make_unique<RealImage>(fileName);
        }
        if (realImage) {
            realImage->display();
        }
    }
};

// Example usage
void demonstrateProxy() {
    std::unique_ptr<Image> image1 = std::make_unique<ImageProxy>("LargePhoto.jpg");
    std::unique_ptr<Image> image2 = std::make_unique<ImageProxy>("AnotherLargePhoto.jpg");

    std::cout << "Images created. No loading occurred yet.\n";
    
    std::cout << "\nDisplaying image 1:\n";
    image1->display(); // RealImage is loaded here
    
    std::cout << "\nDisplaying image 2:\n";
    image2->display(); // RealImage is loaded here
    
    std::cout << "Both images displayed.\n";
}
```

## Behavioral Patterns for Dynamic Interactions

Behavioral design patterns are concerned with algorithms and the assignment of responsibilities between objects. They describe not just patterns of objects or classes but also the patterns of communication between them, enabling more flexible and dynamic interactions [[114]]. These patterns are fundamental to event-driven architectures, game mechanics, and complex business logic. This section details eleven behavioral patterns: Chain of Responsibility, Command, Interpreter, Iterator, Mediator, Strategy, Visitor, Observer, State, Memento, and Template Method. Each pattern is explained with a real-world C++ example relevant to domains like game development, GUI programming, and application scripting.

The **Chain of Responsibility Pattern** allows a request to be passed along a chain of handlers. Upon receiving a request, each handler decides either to process the request or pass it to the next handler in the chain [[134]]. This pattern decouples the sender of a request from its receiver, giving multiple objects a chance to handle the request. A prime real-world example is a multi-level logging system. A log message originating from a game engine could be handled first by a `FileLogger` to save a permanent record, then passed to a `NetworkLogger` to send it to a centralized server, and finally to a `ConsoleLogger` to display it during development [[133]]. Another powerful example is found in GUI toolkits like Qt, whose event propagation system works similarly, where events are passed from widgets up to their parents until an object handles them [[393]]. This pattern is also used in parsing complex expressions or commands, where each link in the chain attempts to interpret a specific part of the input [[232]].

```cpp
#include <iostream>
#include <memory>

// Handler Interface
class Logger {
protected:
    std::unique_ptr<Logger> successor;
public:
    virtual ~Logger() = default;
    void setSuccessor(std::unique_ptr<Logger> nextLogger) {
        successor = std::move(nextLogger);
    }
    virtual void log(int level, const std::string& message) = 0;
    
    void handleLog(int level, const std::string& message) {
        if (canHandle(level)) {
            log(level, message);
        }
        if (successor) {
            successor->handleLog(level, message);
        }
    }
protected:
    virtual bool canHandle(int level) const = 0;
};

// Concrete Handlers
class ConsoleLogger : public Logger {
protected:
    bool canHandle(int level) const override {
        return level == 1; // High priority
    }
public:
    void log(int level, const std::string& message) override {
        std::cout << "=== CONSOLE LOGGER ===\n";
        std::cout << "HIGH PRIORITY: " << message << "\n";
    }
};

class FileLogger : public Logger {
protected:
    bool canHandle(int level) const override {
        return level == 2; // Medium priority
    }
public:
    void log(int level, const std::string& message) override {
        std::cout << "=== FILE LOGGER ===\n";
        std::cout << "MEDIUM PRIORITY: " << message << "\n";
    }
};

class NetworkLogger : public Logger {
protected:
    bool canHandle(int level) const override {
        return level == 3; // Low priority
    }
public:
    void log(int level, const std::string& message) override {
        std::cout << "=== NETWORK LOGGER ===\n";
        std::cout << "LOW PRIORITY: " << message << "\n";
    }
};

// Example usage
void demonstrateChainOfResponsibility() {
    auto consoleLogger = std::make_unique<ConsoleLogger>();
    auto fileLogger = std::make_unique<FileLogger>();
    auto networkLogger = std::make_unique<NetworkLogger>();

    // Construct the chain
    consoleLogger->setSuccessor(std::move(fileLogger));
    consoleLogger->getSuccessor()->setSuccessor(std::move(networkLogger));

    // Process logs
    consoleLogger->handleLog(1, "This is a high-priority error message."); // Handled by ConsoleLogger
    consoleLogger->handleLog(2, "This is a medium-priority info message.");   // Handled by FileLogger
    consoleLogger->handleLog(3, "This is a low-priority debug message.");    // Handled by NetworkLogger
    consoleLogger->handleLog(4, "This is an unknown priority message.");     // Not handled by anyone
}
```

The **Command Pattern** encapsulates a request as an object, thereby letting you parameterize clients with different requests, queue or log requests, and support undoable operations [[28]]. Its most common application is implementing undo/redo functionality in applications like text editors or graphics programs [[30]]. Each action (e.g., typing a character, deleting a word) is wrapped in a `Command` object. This command object knows how to perform the action and, crucially, how to undo it [[31]]. When an action is performed, the command is executed and pushed onto an `executionStack`. To undo, the command is popped from the stack and its `undo()` method is called; the undone command is then pushed onto a `historyStack`. The `QUndoStack` and `QUndoCommand` classes in the Qt framework provide a robust implementation of this pattern for C++ GUI development [[226,228]]. This decouples the object that invokes the operation (the invoker, like a button click) from the object that performs it (the receiver, like the document model).

```cpp
#include <iostream>
#include <vector>
#include <memory>

// Receiver
class TextEditor {
private:
    std::string content;
public:
    void insertText(const std::string& text, int position) {
        content.insert(position, text);
        std::cout << "Text inserted: " << text << " at position " << position << "\n";
    }
    
    void deleteText(int length, int position) {
        if (position + length <= content.length()) {
            content.erase(position, length);
            std::cout << "Text deleted at position " << position << " with length " << length << "\n";
        }
    }
    
    void print() const {
        std::cout << "Current content: '" << content << "'\n";
    }
};

// Command Interface
class Command {
public:
    virtual ~Command() = default;
    virtual void execute() = 0;
    virtual void undo() = 0;
};

// Concrete Commands
class InsertCommand : public Command {
private:
    TextEditor& editor;
    std::string text;
    int position;
public:
    InsertCommand(TextEditor& e, const std::string& t, int p) : editor(e), text(t), position(p) {}
    
    void execute() override {
        editor.insertText(text, position);
    }
    
    void undo() override {
        editor.deleteText(text.length(), position);
    }
};

class DeleteCommand : public Command {
private:
    TextEditor& editor;
    std::string deletedText;
    int position;
    int length;
public:
    DeleteCommand(TextEditor& e, int pos, int len) : editor(e), position(pos), length(len) {
        // We need to know what we're deleting for the undo operation
        // In a real app, the receiver would provide this info
        deletedText = "X"; // Simplified placeholder
    }
    
    void execute() override {
        editor.deleteText(length, position);
    }
    
    void undo() override {
        editor.insertText(deletedText, position);
    }
};

// Invoker
class EditorInvoker {
private:
    std::vector<std::unique_ptr<Command>> history;
    int currentIndex;
public:
    EditorInvoker() : currentIndex(-1) {}
    
    void executeCommand(std::unique_ptr<Command> command) {
        command->execute();
        // Truncate history beyond current index
        history.resize(currentIndex + 1);
        history.push_back(std::move(command));
        currentIndex++;
    }
    
    void undo() {
        if (currentIndex >= 0) {
            history[currentIndex]->undo();
            currentIndex--;
        } else {
            std::cout << "Nothing to undo.\n";
        }
    }
    
    void redo() {
        // Redo is not implemented in this simple example
        std::cout << "Redo not implemented in this simple demo.\n";
    }
};

// Example usage
void demonstrateCommand() {
    TextEditor editor;
    EditorInvoker invoker;
    
    invoker.executeCommand(std::make_unique<InsertCommand>(editor, "Hello ", 0));
    invoker.executeCommand(std::make_unique<InsertCommand>(editor, "World!", 6));
    editor.print(); // 'Hello World!'
    
    invoker.undo();
    editor.print(); // 'Hello '
    
    invoker.undo();
    editor.print(); // ''
}
```

The **Interpreter Pattern** defines a representation for a grammar of a language and an interpreter to interpret sentences in that language [[82]]. While less common in modern applications due to the prevalence of dedicated parsers, it is still relevant for building simple Domain-Specific Languages (DSLs) or evaluating mathematical expressions. A C++ compiler's front end uses this pattern to process the language's syntax [[82]]. For example, one could define a grammar for boolean expressions (e.g., `AND`, `OR`, `NOT`). The pattern involves creating a class hierarchy where each non-terminal expression is represented by a class that contains instances of other expression objects [[365]]. A modern C++ approach would involve using a recursive descent parser or leveraging a library like Boost.Spirit.X3, which essentially implements this pattern in a highly optimized and expressive way [[294]]. The `std::variant` and `std::visit` features introduced in C++17 provide a powerful, type-safe mechanism for traversing and evaluating abstract syntax trees (ASTs), offering a more idiomatic alternative to the traditional recursive visitor pattern in some scenarios [[158,161]].

```cpp
#include <iostream>
#include <memory>
#include <variant>
#include <string>

// Expression is a variant that can hold either an integer or a pointer to another Expression
using Expression = std::variant<int, std::unique_ptr<Expression>>;

// Simplified AST Node for demonstration
class BinaryOperation {
public:
    enum OpType { ADD, SUB };
    OpType op;
    std::unique_ptr<Expression> left, right;
    
    BinaryOperation(OpType o, std::unique_ptr<Expression> l, std::unique_ptr<Expression> r)
        : op(o), left(std::move(l)), right(std::move(r)) {}
};

// Simplified visitor for evaluation
struct Evaluator {
    int visit(int value) {
        return value;
    }
    
    int visit(std::unique_ptr<Expression>& expr) {
        if (auto* binOp = std::get_if<BinaryOperation>(&*expr)) {
            switch (binOp->op) {
                case BinaryOperation::ADD:
                    return std::visit(Evaluator{}, *binOp->left) + std::visit(Evaluator{}, *binOp->right);
                case BinaryOperation::SUB:
                    return std::visit(Evaluator{}, *binOp->left) - std::visit(Evaluator{}, *binOp->right);
            }
        }
        return 0;
    }
};

// Example usage demonstrating the concept
// Note: This is a highly simplified and incomplete example to illustrate the principle.
// A full implementation would require a robust parser and a more extensive AST.
void demonstrateInterpreterConcept() {
    // Creates a simple AST for (5 + 3) - 2
    auto expr = std::make_unique<Expression>(
        std::make_unique<BinaryOperation>(
            BinaryOperation::SUB,
            std::make_unique<Expression>(
                std::make_unique<BinaryOperation>(
                    BinaryOperation::ADD,
                    std::make_unique<Expression>(5),
                    std::make_unique<Expression>(3)
                )
            ),
            std::make_unique<Expression>(2)
        )
    );
    
    // Evaluate the expression
    Evaluator evaluator;
    int result = std::visit(evaluator, *expr);
    std::cout << "Result of (5 + 3) - 2 is: " << result << "\n"; // Output: 6
}
```

The **Iterator Pattern** provides a way to access the elements of an aggregate object sequentially without exposing its underlying representation [[118]]. The standard C++ iterator concept is the canonical example of this pattern. It allows algorithms to work with containers (like `std::vector` or `std::list`) without knowing their internal storage details (e.g., array vs. linked list). A custom iterator can be implemented to traverse complex data structures like a composite tree or a binary search tree. Using the Boost.IteratorAdaptor library simplifies this process by handling much of the boilerplate required for a compliant iterator [[126]]. The C++20 Ranges library further enhances this concept by providing a more declarative and composable way to process sequences, combining iteration and algorithms into a single pipeline using views [[118]]. This pattern is essential for writing generic algorithms that can operate on a wide variety of container types.

```cpp
#include <iostream>
#include <vector>
#include <memory>

// Aggregate (Container)
class NumberCollection {
private:
    std::vector<int> numbers;
public:
    explicit NumberCollection(const std::vector<int>& n) : numbers(n) {}
    
    // Iterator class
    class Iterator {
    private:
        std::vector<int>::iterator current;
        std::vector<int>::iterator endIter;
    public:
        explicit Iterator(std::vector<int>::iterator start, std::vector<int>::iterator end)
            : current(start), endIter(end) {}
        
        void operator++() {
            if (current != endIter) {
                ++current;
            }
        }
        
        bool operator!=(const Iterator& other) const {
            return current != other.current;
        }
        
        int operator*() const {
            return *current;
        }
    };
    
    Iterator begin() {
        return Iterator(numbers.begin(), numbers.end());
    }
    
    Iterator end() {
        return Iterator(numbers.end(), numbers.end());
    }
};

// Example usage
void demonstrateIterator() {
    NumberCollection collection({1, 2, 3, 4, 5});
    
    std::cout << "Iterating through collection: ";
    for (auto it = collection.begin(); it != collection.end(); ++it) {
        std::cout << *it << " ";
    }
    std::cout << "\n";
}
```

The **Mediator Pattern** defines an object that encapsulates how a set of objects interact. It promotes loose coupling by preventing objects from referring to each other explicitly, and it centralizes the control of complex interactions [[84]]. A classic example is a chat room [[83]]. Users don't send messages directly to each other; instead, they send them to the `ChatRoom` mediator, which then broadcasts the message to all other participants. This decouples the user objects completely. In a GUI application, a complex dialog box with many controls (text fields, buttons, checkboxes) can be managed by a mediator. Instead of each control needing to know about the others to enable/disable them or update their state, they all communicate through the mediator, which contains the business logic for their interactions [[257]]. This pattern is also present in the Model/View architecture of frameworks like Qt, where the view and model communicate indirectly through the controller [[166]].

```cpp
#include <iostream>
#include <string>
#include <vector>
#include <memory>

// Colleague Base Class
class UIControl {
protected:
    std::shared_ptr<UIWidgetMediator> mediator;
    std::string name;
public:
    UIControl(const std::string& n, std::shared_ptr<UIWidgetMediator> m) : name(n), mediator(m) {}
    virtual ~UIControl() = default;
    virtual void onChange() = 0;
    const std::string& getName() const { return name; }
};

// Concrete Colleagues
class TextBox : public UIControl {
private:
    std::string text;
public:
    explicit TextBox(const std::string& n, std::shared_ptr<UIWidgetMediator> m) : UIControl(n, m) {}
    
    void setText(const std::string& t) {
        text = t;
        onChange();
    }
    
    void onChange() override {
        mediator->valueChanged(this);
    }
};

class Button : public UIControl {
private:
    bool enabled;
public:
    explicit Button(const std::string& n, std::shared_ptr<UIWidgetMediator> m) : UIControl(n, m), enabled(false) {}
    
    void setEnabled(bool e) {
        enabled = e;
        // In a real UI, this would update the button's appearance
    }
    
    bool isEnabled() const { return enabled; }
};

// Mediator Interface
class UIWidgetMediator {
public:
    virtual void valueChanged(UIControl* control) = 0;
    virtual ~UIWidgetMediator() = default;
};

// Concrete Mediator
class FormMediator : public UIWidgetMediator {
private:
    std::shared_ptr<TextBox> textBox;
    std::shared_ptr<Button> button;
public:
    FormMediator(std::shared_ptr<TextBox> t, std::shared_ptr<Button> b)
        : textBox(std::move(t)), button(std::move(b)) {}
    
    void valueChanged(UIControl* control) override {
        if (control == textBox.get()) {
            if (!textBox->getText().empty()) {
                button->setEnabled(true);
            } else {
                button->setEnabled(false);
            }
        }
    }
};

// Example usage
void demonstrateMediator() {
    auto textBox = std::make_shared<TextBox>("UsernameBox", nullptr);
    auto button = std::make_shared<Button>("SubmitButton", nullptr);
    
    auto mediator = std::make_shared<FormMediator>(textBox, button);
    textBox->mediator = mediator;
    button->mediator = mediator;
    
    std::cout << "Form initialized. Submit button should be disabled.\n";
    std::cout << "Is submit button enabled? " << (button->isEnabled() ? "Yes" : "No") << "\n";
    
    textBox->setText("user123");
    std::cout << "After entering text, submit button should be enabled.\n";
    std::cout << "Is submit button enabled? " << (button->isEnabled() ? "Yes" : "No") << "\n";
}
```

The **Strategy Pattern** defines a family of algorithms, encapsulates each one, and makes them interchangeable [[142]]. It lets the algorithm vary independently from clients that use it. This is perfect for scenarios requiring different implementations of an operation, such as sorting algorithms, compression strategies, or payment methods. A `Sorter` class could take a `SortingStrategy` object in its constructor and delegate the sorting logic to it [[38]]. The strategy can be changed at runtime, allowing the client to alter the object's behavior dynamically [[251]]. In modern C++, this pattern is often implemented concisely using `std::function` and lambdas, which can hold any callable object, including functions, functors, and lambda expressions [[282]]. This avoids the need for a formal `Strategy` base class and derived classes for simple strategies. A practical example is a video player that can apply different color correction filters (a `FilterStrategy`) to a video stream in real-time [[141]].

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
#include <functional>

// Strategy Interface (as a type alias for a callable)
using SortStrategy = std::function<void(std::vector<int>&)>;

// Concrete Strategies
void bubbleSort(std::vector<int>& data) {
    std::cout << "Applying Bubble Sort.\n";
    // Simple bubble sort implementation
    for (size_t i = 0; i < data.size(); ++i) {
        for (size_t j = 0; j < data.size() - 1; ++j) {
            if (data[j] > data[j + 1]) {
                std::swap(data[j], data[j + 1]);
            }
        }
    }
}

void quickSort(std::vector<int>& data) {
    std::cout << "Applying Quick Sort.\n";
    // Simple quick sort implementation using STL
    std::sort(data.begin(), data.end());
}

// Context
class Sorter {
private:
    SortStrategy strategy;
public:
    explicit Sorter(SortStrategy s) : strategy(std::move(s)) {}
    
    void sort(std::vector<int>& data) {
        if (strategy) {
            strategy(data);
        }
    }
};

// Example usage
void demonstrateStrategy() {
    std::vector<int> numbers = {64, 34, 25, 12, 22, 11, 90};
    
    std::cout << "Original array: ";
    for (int n : numbers) std::cout << n << " ";
    std::cout << "\n\n";
    
    Sorter bubbleSorter(bubbleSort);
    Sorter quickSorter(quickSort);
    
    bubbleSorter.sort(numbers);
    std::cout << "Array after Bubble Sort: ";
    for (int n : numbers) std::cout << n << " ";
    std::cout << "\n\n";
    
    quickSorter.sort(numbers);
    std::cout << "Array after Quick Sort: ";
    for (int n : numbers) std::cout << n << " ";
    std::cout << "\n";
}
```

The **Visitor Pattern** separates an algorithm from the object structure on which it operates. It allows you to define new operations without changing the classes of the elements on which it operates [[40]]. This is extremely useful for adding functionality to a class hierarchy that you cannot modify directly. A classic example is traversing an Abstract Syntax Tree (AST) in a compiler, where a visitor can be created to perform different tasks like code generation, type checking, or optimization [[82]]. Each node in the tree (e.g., `BinaryExpression`, `Literal`, `VariableDeclaration`) would have an `accept(Visitor& v)` method. The visitor would have an overloaded `visit()` method for each node type. C++17's `std::variant` and `std::visit` provide a modern, type-safe, and often more concise way to achieve the same effect as the traditional recursive visitor pattern [[158,161]]. The `std::visit` function dispatches to the correct overload based on the type currently held in the `std::variant`, effectively implementing the double-dispatch mechanism required by the visitor pattern [[162]].

```cpp
#include <iostream>
#include <memory>
#include <variant>

// Forward declarations for the Variant-based AST
class BinaryExpr;
class Literal;

// Define the AST node as a variant
using AstNode = std::variant<std::unique_ptr<BinaryExpr>, std::unique_ptr<Literal>>;

// Concrete Element: Literal
class Literal {
public:
    int value;
    explicit Literal(int v) : value(v) {}
};

// Concrete Element: BinaryExpr
class BinaryExpr {
public:
    std::unique_ptr<AstNode> left;
    std::unique_ptr<AstNode> right;
    char op;
    BinaryExpr(std::unique_ptr<AstNode> l, char o, std::unique_ptr<AstNode> r)
        : left(std::move(l)), right(std::move(r)), op(o) {}
};

// Concrete Visitor
struct Evaluator {
    int visit(const Literal& literal) {
        return literal.value;
    }
    
    int visit(const BinaryExpr& expr) {
        int leftVal = std::visit(*this, *expr.left);
        int rightVal = std::visit(*this, *expr.right);
        switch (expr.op) {
            case '+': return leftVal + rightVal;
            case '-': return leftVal - rightVal;
            case '*': return leftVal * rightVal;
            default: return 0;
        }
    }
};

// Example usage
void demonstrateVisitorWithVariant() {
    // Constructs an AST for ((1 + 2) * 3)
    auto ast = std::make_unique<AstNode>(
        std::make_unique<BinaryExpr>(
            std::make_unique<AstNode>(std::make_unique<Literal>(1)),
            '+',
            std::make_unique<AstNode>(std::make_unique<Literal>(2))
        )
    );
    
    // Add the multiplier
    auto finalAst = std::make_unique<AstNode>(
        std::make_unique<BinaryExpr>(
            std::move(*ast),
            '*',
            std::make_unique<AstNode>(std::make_unique<Literal>(3))
        )
    );
    
    Evaluator evaluator;
    int result = std::visit(evaluator, **finalAst);
    std::cout << "Result of evaluating the AST is: " << result << "\n"; // Output: 9
}
```

The **Observer Pattern** defines a one-to-many dependency between objects so that when one object changes state, all its dependents are notified automatically [[115]]. This is the foundation of event-driven systems. A publisher (subject) maintains a list of its dependents (observers) and notifies them of any state changes by calling their update() method. Qt's signals and slots mechanism is a prominent and robust implementation of this pattern in C++ [[293,389]]. When an object's state changes, it emits a signal, which is connected to one or more slots (observer methods) that react to the event. This decouples the publisher from the observers, as the publisher doesn't need to know anything about the observer's implementation. Another common use case is in GUI applications, where a model (data source) notifies its views (UI components) whenever the data changes, ensuring the UI remains synchronized [[288]]. Using smart pointers like `std::weak_ptr` is crucial for implementing thread-safe observers to prevent dangling pointers and circular references [[377,378]].

```cpp
#include <iostream>
#include <vector>
#include <memory>
#include <algorithm>

// Observer Interface
class Observer {
public:
    virtual ~Observer() = default;
    virtual void update(const std::string& message) = 0;
};

// Subject (Observable) Interface
class Subject {
public:
    virtual ~Subject() = default;
    virtual void attach(std::unique_ptr<Observer> observer) = 0;
    virtual void detach(Observer* observer) = 0;
    virtual void notify(const std::string& message) = 0;
};

// Concrete Subject
class JobStatusPublisher : public Subject {
private:
    std::vector<std::unique_ptr<Observer>> observers;
public:
    void attach(std::unique_ptr<Observer> observer) override {
        observers.push_back(std::move(observer));
    }
    
    void detach(Observer* observerToRemove) override {
        observers.erase(
            std::remove_if(observers.begin(), observers.end(),
                [observerToRemove](const std::unique_ptr<Observer>& observer) {
                    return observer.get() == observerToRemove;
                }),
            observers.end()
        );
    }
    
    void notify(const std::string& message) override {
        for (const auto& observer : observers) {
            observer->update(message);
        }
    }
};

// Concrete Observers
class EmailNotifier : public Observer {
public:
    void update(const std::string& message) override {
        std::cout << "EmailNotifier: Sending email notification for status: " << message << "\n";
    }
};

class CacheInvalidator : public Observer {
public:
    void update(const std::string& message) override {
        if (message == "JOB_COMPLETED") {
            std::cout << "CacheInvalidator: Invalidating cache due to job completion.\n";
        }
    }
};

// Example usage
void demonstrateObserver() {
    JobStatusPublisher jobPublisher;
    EmailNotifier emailNotifier;
    CacheInvalidator cacheInvalidator;
    
    jobPublisher.attach(std::make_unique<EmailNotifier>());
    jobPublisher.attach(std::make_unique<CacheInvalidator>());
    
    std::cout << "Job started...\n";
    jobPublisher.notify("JOB_STARTED");
    
    std::cout << "\nJob completed!\n";
    jobPublisher.notify("JOB_COMPLETED");
    
    std::cout << "\nDetaching email notifier.\n";
    jobPublisher.detach(&emailNotifier);
    
    std::cout << "Job failed...\n";
    jobPublisher.notify("JOB_FAILED");
}
```

The **State Pattern** allows an object to alter its behavior when its internal state changes. The object will appear to change its class [[35]]. This pattern is a cleaner alternative to large state machines implemented with switch statements or long if-else chains over a state variable [[37]]. An excellent real-world example is managing the state of an e-commerce order. An `Order` object can be in states like `Pending`, `Shipped`, or `Delivered`. Instead of a switch statement in the `process()` method, the `Order` class would hold a pointer to a `State` interface. Each concrete state class (`PendingState`, `ShippedState`) would implement the `process()` method according to the rules of that state. When an event occurs (e.g., the order is shipped), the `Order` object's state pointer is replaced with a new state object, and subsequent calls to `process()` will be delegated to the new state's implementation. This keeps the state-specific logic encapsulated within the state classes and makes the `Order` class cleaner and more maintainable [[142]].

```cpp
#include <iostream>
#include <memory>

// State Interface
class OrderState {
public:
    virtual ~OrderState() = default;
    virtual void handle(OrderState& order) = 0;
};

// Concrete States
class PendingState : public OrderState {
public:
    void handle(OrderState& order) override {
        std::cout << "Order is pending. Customer can cancel it.\n";
        // Transition logic
        std::cout << "Transitioning to ShippedState.\n";
        order.setState(std::make_unique<ShippedState>());
    }
};

class ShippedState : public OrderState {
public:
    void handle(OrderState& order) override {
        std::cout << "Order has been shipped. Customer can track it.\n";
        // Transition logic
        std::cout << "Transitioning to DeliveredState.\n";
        order.setState(std::make_unique<DeliveredState>());
    }
};

class DeliveredState : public OrderState {
public:
    void handle(OrderState& order) override {
        std::cout << "Order has been delivered. Customer can leave a review.\n";
        // No further transitions
    }
};

// Context
class OrderContext {
private:
    std::unique_ptr<OrderState> state;
public:
    OrderContext() {
        state = std::make_unique<PendingState>();
    }
    
    void setState(std::unique_ptr<OrderState> newState) {
        state = std::move(newState);
    }
    
    void handle() {
        if (state) {
            state->handle(*this);
        }
    }
};

// Example usage
void demonstrateState() {
    OrderContext order;
    
    std::cout << "=== Order Lifecycle ===\n";
    for (int i = 0; i < 3; ++i) {
        order.handle();
    }
}
```

The **Memento Pattern** captures and externalizes an object's internal state without violating encapsulation, so the object can be restored to this state later . It is intrinsically linked with the Command pattern and is the key to implementing save/load and undo/redo features. The pattern involves three roles: the `Originator` (the object whose state is to be saved), the `Memento` (an opaque object containing the saved state), and the `Caretaker` (responsible for storing the memento). The `Originator` creates a memento containing a snapshot of its current state and can restore its state from a memento provided by the caretaker. A `QUndoCommand` in Qt, for example, saves a memento of the document's state before it was modified; upon undoing, it restores the state from that memento [[137,533]]. This pattern cleanly separates the process of saving and restoring state from the business logic of the object itself.

```cpp
#include <iostream>
#include <string>
#include <memory>

// Memento
class Memento {
private:
    std::string state;
    
    // Originator can access private members
    friend class TextEditor;
    
    explicit Memento(const std::string& s) : state(s) {}
    
public:
    std::string getState() const {
        return state;
    }
};

// Originator
class TextEditor {
private:
    std::string content;
public:
    void setContent(const std::string& text) {
        content = text;
        std::cout << "Editor content set to: " << content << "\n";
    }
    
    std::unique_ptr<Memento> createMemento() {
        std::cout << "Creating a memento of the current content.\n";
        return std::make_unique<Memento>(content);
    }
    
    void restoreFromMemento(const Memento& memento) {
        content = memento.state;
        std::cout << "Editor content restored from memento: " << content << "\n";
    }
};

// Caretaker
class History {
private:
    std::vector<std::unique_ptr<Memento>> states;
    int currentStateIndex;
public:
    History() : currentStateIndex(-1) {}
    
    void saveState(const std::unique_ptr<Memento>& memento) {
        // Trim forward history if we restored from an older state
        states.resize(currentStateIndex + 1);
        states.push_back(memento->clone());
        currentStateIndex++;
    }
    
    bool canUndo() const {
        return currentStateIndex >= 0;
    }
    
    std::unique_ptr<Memento> undo() {
        if (canUndo()) {
            std::unique_ptr<Memento> stateToRestore = states[currentStateIndex]->clone();
            currentStateIndex--;
            return stateToRestore;
        }
        return nullptr;
    }
};

// Example usage
void demonstrateMemento() {
    TextEditor editor;
    History history;
    
    editor.setContent("First version.");
    history.saveState(editor.createMemento());
    
    editor.setContent("Second version.");
    history.saveState(editor.createMemento());
    
    editor.setContent("Third version.");
    std::cout << "Current editor content: " << editor.getContent() << "\n";
    
    if (history.canUndo()) {
        auto memento = history.undo();
        if (memento) {
            editor.restoreFromMemento(*memento);
        }
    }
    
    if (history.canUndo()) {
        auto memento = history.undo();
        if (memento) {
            editor.restoreFromMemento(*memento);
        }
    }
}
```

The **Template Method Pattern** defines the skeleton of an algorithm in a method, deferring some steps to subclasses. It lets subclasses redefine certain steps of an algorithm without changing the algorithm's structure [[89]]. This is a classic "inversion of control" pattern where the superclass controls the overall flow. A common example is a `DocumentProcessor` base class that defines a template method `parseAndSave()`. This method might call `parse()`, `validate()`, and `save()` in sequence. Subclasses like `HtmlDocumentProcessor` and `PdfDocumentProcessor` can then override the `parse()` and `save()` methods to provide their specific implementations, while reusing the unchanged algorithm structure from the base class [[339,518]]. This pattern is widely used in frameworks to allow customization points. In Qt, many base classes provide template methods that developers can hook into by subclassing and overriding protected virtual functions [[236]].

```cpp
#include <iostream>
#include <memory>

// Abstract Class (Base Class)
class GameCharacter {
public:
    // Template Method
    void playTurn() {
        std::cout << "GameCharacter::playTurn() - Starting turn.\n";
        prepareAction();
        executeAction();
        endTurn();
    }
    
protected:
    virtual void prepareAction() {
        std::cout << "Preparing a generic action.\n";
    }
    
    virtual void executeAction() = 0; // Abstract step
    
    virtual void endTurn() {
        std::cout << "Ending turn. Moving to next player.\n";
    }
};

// Concrete Class 1
class Warrior : public GameCharacter {
protected:
    void prepareAction() override {
        std::cout << "Warrior preparing to attack.\n";
    }
    
    void executeAction() override {
        std::cout << "Warrior swings sword!\n";
    }
};

// Concrete Class 2
class Mage : public GameCharacter {
protected:
    void prepareAction() override {
        std::cout << "Mage is casting a spell.\n";
    }
    
    void executeAction() override {
        std::cout << "Mage casts Fireball!\n";
    }
    
    void endTurn() override {
        std::cout << "Mage's mana is depleted. Ending turn early.\n";
    }
};

// Example usage
void demonstrateTemplateMethod() {
    std::unique_ptr<GameCharacter> warrior = std::make_unique<Warrior>();
    std::unique_ptr<GameCharacter> mage = std::make_unique<Mage>();
    
    std::cout << "=== Starting Warrior's Turn ===\n";
    warrior->playTurn();
    
    std::cout << "\n=== Starting Mage's Turn ===\n";
    mage->playTurn();
}
```

## Synthesis and Practical Integration for Web-Based Learning

This report has systematically detailed 23 canonical design patterns, providing deep descriptions and practical C++ examples grounded in real-world contexts such as game development, high-performance networking, and UI frameworks. The selection of patterns covers the three main categories—Creational, Structural, and Behavioral—as requested, fulfilling the core research goal of generating content suitable for an educational web application. The emphasis on realistic scenarios, such as using the State pattern for game character states [[37]], the Command pattern for undo/redo in a document editor [[31]], and the Bridge pattern to decouple a rendering engine from its backend APIs [[211]], ensures that the material moves beyond theoretical constructs and addresses tangible engineering problems. The provided C++ code examples are designed to be self-contained, pedagogically effective, and directly integrable into an interactive learning platform.

The practical integration of this content into a web-based demonstration platform hinges on several key technologies and architectural decisions identified through the analysis of the provided sources. The primary technical enabler for achieving interactivity is **WebAssembly (Wasm)**. Wasm allows C++ code to be compiled and run in a browser at near-native speed, bypassing the limitations of JavaScript for performance-critical tasks [[307,480]]. Tools like **Emscripten** provide a mature toolchain to compile C++ code into a `.wasm` module and a corresponding JavaScript "glue" file that facilitates interoperability [[125,428]]. This architecture is perfectly suited for the proposed application: a developer could edit the C++ code of a pattern's demonstration in a browser-based code editor (like Monaco, used by VS Code), and upon clicking a "Run" button, the application would use Emscripten's JS API to instantiate the Wasm module and display the program's output within the page [[452]]. This creates a truly live, interactive sandbox for experimentation, a feature highlighted as desirable for AI-assisted coding environments [[360]].

The structure of the web application itself should mirror the pedagogical clarity of the content. A central navigation menu should categorize the patterns into Creational, Structural, and Behavioral sections, as done in this report. Upon selecting a pattern, the user should be presented with a dedicated documentation page. This page should be structured to guide the learner logically through the concept, following a proven instructional design model :
1.  **Intent & Motivation:** A clear, concise summary of the problem the pattern solves and why a developer would choose to use it.
2.  **Real-World Context:** A brief explanation of the domain where the pattern is most applicable (e.g., Game Development, Networking, UI).
3.  **Before & After Code Comparison:** Side-by-side code snippets showcasing a naive implementation (e.g., a long switch statement or direct object creation) versus the implementation using the pattern. This contrast is crucial for demonstrating the benefits of refactoring .
4.  **Interactive C++ Example:** The complete, commented C++ code, running inside the WebAssembly-powered sandbox. Interactive toggles could even allow users to switch between different implementations, such as choosing a sorting algorithm in a Strategy pattern demo [[146]].
5.  **Pros & Cons:** A balanced discussion of the trade-offs, highlighting increased complexity versus gains in flexibility, maintainability, or scalability. Anti-pattern warnings, such as those against creating "God Objects" with Singletons [[73]] or over-engineering with unnecessary adapters [[48]], are vital for responsible learning.

Furthermore, the project's long-term viability and community engagement depend on adopting modern open-source practices. The repository should be organized with a clear, scalable directory structure, separating application logic, tests, and documentation . The use of a CI/CD pipeline, powered by GitHub Actions, is essential for maintaining quality. This pipeline should automatically run a linter (like `ruff` for Python, or its C++ equivalent) and formatter (`black` or `clang-format`) on every pull request, ensuring code quality is maintained at the source . A comprehensive test suite, covering both unit tests for the pattern logic and integration tests for the web application's routing and rendering, is critical for reliability [[545]]. Finally, providing clear contribution guidelines (`CONTRIBUTING.md`) and documentation templates will lower the barrier to entry for new contributors, fostering a healthy ecosystem around the project . The modularity of the pattern registry architecture described in the initial plan  ensures that adding new patterns is a straightforward process, allowing the educational resource to grow and remain relevant over time. By combining these robust C++ examples with a modern, interactive web delivery platform and sound open-source governance, this project can become a definitive resource for teaching and learning software design patterns.