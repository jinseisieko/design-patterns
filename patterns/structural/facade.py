"""Facade Pattern Demonstration (C++).

Real-world context: Database manager - providing a simplified interface to a
complex subsystem of connection pools, query parsers, and transaction managers.

Anti-pattern warning: God Object facade - Creating a facade that becomes a
monolithic class with too many responsibilities.
"""

CPP_CODE = r"""#include <iostream>
#include <string>

// Subsystem Classes
class ConnectionPool {
public:
    void init() { std::cout << "Initializing connection pool.\n"; }
    Connection getConnection() { 
        std::cout << "Getting connection from pool.\n";
        return Connection{};
    }
    void release(Connection c) { std::cout << "Releasing connection.\n"; }
};

class QueryParser {
public:
    Query parse(const std::string& query) {
        std::cout << "Parsing: " << query << "\n";
        return Query{query};
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
    ConnectionPool pool;
    QueryParser parser;
    TransactionManager txManager;

public:
    void connect() { pool.init(); }
    
    void disconnect() { 
        std::cout << "Disconnecting from database.\n";
    }
    
    bool executeUpdate(const std::string& query) {
        txManager.begin();
        try {
            auto q = parser.parse(query);
            auto conn = pool.getConnection();
            std::cout << "Executing: " << q.sql << "\n";
            pool.release(conn);
            txManager.commit();
            return true;
        } catch (...) {
            txManager.rollback();
            return false;
        }
    }
    
    std::string querySingle(const std::string& sql) {
        auto conn = pool.getConnection();
        auto q = parser.parse(sql);
        std::cout << "Executing query: " << q.sql << "\n";
        pool.release(conn);
        return "result_data";
    }
};

int main() {
    DatabaseFacade db;
    db.connect();
    
    db.executeUpdate("INSERT INTO users (name) VALUES ('Alice')");
    auto result = db.querySingle("SELECT * FROM users WHERE id=1");
    
    db.disconnect();
}"""

BEFORE_CODE = r"""// Without Facade - client coordinates all subsystems
void saveUser(const User& user) {
    ConnectionPool pool;
    pool.init();
    
    TransactionManager tx;
    tx.begin();
    
    QueryParser parser;
    auto q = parser.parse("INSERT INTO users...");
    
    auto conn = pool.getConnection();
    conn.execute(q);
    pool.release(conn);
    
    tx.commit();
    // Client must know all the details
}"""

AFTER_CODE = r"""// With Facade - simple interface
void saveUser(const User& user) {
    DatabaseFacade db;
    db.connect();
    db.executeUpdate("INSERT INTO users (name) VALUES ('" + user.name + "')");
    db.disconnect();
}"""


def demonstrate() -> dict:
    """Execute the Facade pattern demonstration."""
    return {
        "cpp_code": CPP_CODE,
        "before_code": BEFORE_CODE,
        "after_code": AFTER_CODE,
        "intent": (
            "Provides a unified interface to a subsystem of interfaces, making "
            "the subsystem easier to use."
        ),
        "context": (
            "Database manager - simplifying complex interactions with connection "
            "pools, query parsers, and transaction managers."
        ),
        "pros": [
            "Simplifies interface for common use cases",
            "Reduces dependencies on subsystem internals",
            "Promotes loose coupling between client and subsystem",
        ],
        "cons": [
            "Facade can become a God Object if not carefully designed",
            "May hide useful advanced features from clients",
        ],
        "anti_pattern": (
            "God Object Facade: Don't create a facade that manages too many "
            "unrelated subsystems. Keep facades focused on a specific domain "
            "or use case."
        ),
        "uml_diagram": """
┌─────────────────────┐
│  DatabaseFacade     │
├─────────────────────┤
│ -ConnectionPool     │
│ -QueryParser        │
│ -TransactionManager │
├─────────────────────┤
│ +connect()          │
│ +disconnect()       │
│ +executeUpdate()    │
│ +querySingle()      │
└─────────┬───────────┘
          │ uses
    ┌─────┼─────────────────────┐
    ▼     ▼                     ▼
┌──────┐ ┌────┐          ┌─────────────┐
│ Pool │ │Qry │          │ Transaction │
└──────┘ └────┘          └─────────────┘""",
    }
