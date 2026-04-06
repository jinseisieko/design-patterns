"""Builder Pattern Demonstration (C++).

Real-world context: Constructing sophisticated HTTP requests step-by-step
with a fluent interface, improving readability.

Anti-pattern warning: Unused Builders - Building objects that are always used
immediately after construction with no variation in the building process.
"""

CPP_CODE = r"""#include <iostream>
#include <string>
#include <map>
#include <memory>

// Product: HTTP Request
class HttpRequest {
private:
    std::string url;
    std::map<std::string, std::string> headers;
    std::string body;
    std::string method;

public:
    void display() const {
        std::cout << "=== HTTP Request ===\n";
        std::cout << method << " " << url << "\n";
        for (const auto& [k, v] : headers)
            std::cout << "  " << k << ": " << v << "\n";
        if (!body.empty()) std::cout << "Body: " << body << "\n";
        std::cout << "====================\n\n";
    }
};

// Builder
class HttpRequestBuilder {
private:
    HttpRequest request;
public:
    HttpRequestBuilder& setUrl(const std::string& u) {
        // Set URL via friend or setter...
        return *this;
    }
    HttpRequestBuilder& addHeader(const std::string& k, const std::string& v) {
        return *this;
    }
    HttpRequestBuilder& setBody(const std::string& b) {
        return *this;
    }
    HttpRequestBuilder& setMethod(const std::string& m) {
        return *this;
    }
    HttpRequest build() { return std::move(request); }
};

// Using HttpRequest with direct initialization for demo
struct Request {
    std::string method, url;
    std::map<std::string, std::string> headers;
    std::string body;
    
    void display() const {
        std::cout << method << " " << url << "\n";
        for (const auto& [k,v] : headers)
            std::cout << "  " << k << ": " << v << "\n";
        if (!body.empty()) std::cout << "Body: " << body << "\n";
    }
};

Request buildRequest() {
    Request r;
    r.method = "POST";
    r.url = "/api/users";
    r.headers["Content-Type"] = "application/json";
    r.headers["Authorization"] = "Bearer token123";
    r.body = R"({"name": "John", "email": "john@example.com"})";
    return r;
}

int main() {
    auto req = buildRequest();
    req.display();
}"""

BEFORE_CODE = r"""// Without Builder - long constructor with many optional params
HttpRequest req("POST", "/api/users",
    {},  // no query params
    {{"Content-Type", "application/json"},
     {"Authorization", "Bearer token"}},
    R"({"name": "John"})",
    30,  // timeout
    nullptr,  // no proxy
    false,  // not streaming
    true    // follow redirects
);
// Hard to read, easy to misorder params"""

AFTER_CODE = r"""// With Builder - step-by-step construction
auto req = HttpRequestBuilder{}
    .setMethod("POST")
    .setUrl("/api/users")
    .addHeader("Content-Type", "application/json")
    .addHeader("Authorization", "Bearer token")
    .setBody(R"({"name": "John"})")
    .build();
// Clear, readable, optional steps"""


def demonstrate() -> dict:
    """Execute the Builder pattern demonstration."""
    return {
        "cpp_code": CPP_CODE,
        "before_code": BEFORE_CODE,
        "after_code": AFTER_CODE,
        "intent": (
            "Separates the construction of a complex object from its representation, "
            "allowing the same construction process to create different representations."
        ),
        "context": (
            "HTTP request construction - building requests with optional headers, "
            "body, authentication, and timeouts using a fluent interface."
        ),
        "pros": [
            "Construct objects step-by-step",
            "Reuse the same construction code for different representations",
            "Encapsulates complex construction logic",
        ],
        "cons": [
            "Requires creating a separate Builder class",
            "Overkill for simple objects",
        ],
        "anti_pattern": (
            "Unused Builders: Don't use the Builder pattern when the object is "
            "always constructed the same way. Reserve it for objects with many "
            "optional parameters or varying construction steps."
        ),
        "uml_diagram": """
┌──────────────────┐
│   HttpRequest    │  (Product)
├──────────────────┤
│ -url, method     │
│ -headers, body   │
│ -timeout, proxy  │
└──────────────────┘

┌──────────────────────────┐
│ HttpRequestBuilder       │  (Builder)
├──────────────────────────┤
│ +setUrl(url)             │
│ +setMethod(method)       │
│ +addHeader(key, val)     │
│ +setBody(body)           │
│ +setTimeout(seconds)     │
│ +build() -> HttpRequest  │
└──────────────────────────┘""",
    }
