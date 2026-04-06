"""Integration tests for Flask application routes."""


class TestIndexRoute:
    """Test cases for index route."""

    def test_index_returns_200(self, client):
        """Test index page returns 200 status."""
        response = client.get("/")
        assert response.status_code == 200

    def test_index_renders_template(self, client):
        """Test index page renders correctly."""
        response = client.get("/")
        assert b"23 Essential C++ Design Patterns" in response.data


class TestPatternRoutes:
    """Test cases for pattern demonstration routes."""

    # Creational patterns
    def test_singleton_route(self, client):
        """Test singleton pattern route."""
        response = client.get("/pattern/creational/singleton")
        assert response.status_code == 200
        assert b"Singleton" in response.data

    def test_factory_method_route(self, client):
        """Test factory method pattern route."""
        response = client.get("/pattern/creational/factory_method")
        assert response.status_code == 200
        assert b"Factory Method" in response.data

    def test_abstract_factory_route(self, client):
        """Test abstract factory pattern route."""
        response = client.get("/pattern/creational/abstract_factory")
        assert response.status_code == 200
        assert b"Abstract Factory" in response.data

    def test_builder_route(self, client):
        """Test builder pattern route."""
        response = client.get("/pattern/creational/builder")
        assert response.status_code == 200
        assert b"Builder" in response.data

    def test_prototype_route(self, client):
        """Test prototype pattern route."""
        response = client.get("/pattern/creational/prototype")
        assert response.status_code == 200
        assert b"Prototype" in response.data

    # Structural patterns
    def test_decorator_route(self, client):
        """Test decorator pattern route."""
        response = client.get("/pattern/structural/decorator")
        assert response.status_code == 200
        assert b"Decorator" in response.data

    def test_adapter_route(self, client):
        """Test adapter pattern route."""
        response = client.get("/pattern/structural/adapter")
        assert response.status_code == 200
        assert b"Adapter" in response.data

    def test_bridge_route(self, client):
        """Test bridge pattern route."""
        response = client.get("/pattern/structural/bridge")
        assert response.status_code == 200
        assert b"Bridge" in response.data

    def test_composite_route(self, client):
        """Test composite pattern route."""
        response = client.get("/pattern/structural/composite")
        assert response.status_code == 200
        assert b"Composite" in response.data

    def test_facade_route(self, client):
        """Test facade pattern route."""
        response = client.get("/pattern/structural/facade")
        assert response.status_code == 200
        assert b"Facade" in response.data

    def test_flyweight_route(self, client):
        """Test flyweight pattern route."""
        response = client.get("/pattern/structural/flyweight")
        assert response.status_code == 200
        assert b"Flyweight" in response.data

    def test_proxy_route(self, client):
        """Test proxy pattern route."""
        response = client.get("/pattern/structural/proxy")
        assert response.status_code == 200
        assert b"Proxy" in response.data

    # Behavioral patterns
    def test_strategy_route(self, client):
        """Test strategy pattern route."""
        response = client.get("/pattern/behavioral/strategy")
        assert response.status_code == 200
        assert b"Strategy" in response.data

    def test_observer_route(self, client):
        """Test observer pattern route."""
        response = client.get("/pattern/behavioral/observer")
        assert response.status_code == 200
        assert b"Observer" in response.data

    def test_command_route(self, client):
        """Test command pattern route."""
        response = client.get("/pattern/behavioral/command")
        assert response.status_code == 200
        assert b"Command" in response.data

    def test_state_route(self, client):
        """Test state pattern route."""
        response = client.get("/pattern/behavioral/state")
        assert response.status_code == 200
        assert b"State" in response.data

    def test_chain_of_responsibility_route(self, client):
        """Test chain of responsibility pattern route."""
        response = client.get("/pattern/behavioral/chain_of_responsibility")
        assert response.status_code == 200
        assert b"Chain of Responsibility" in response.data

    def test_interpreter_route(self, client):
        """Test interpreter pattern route."""
        response = client.get("/pattern/behavioral/interpreter")
        assert response.status_code == 200
        assert b"Interpreter" in response.data

    def test_iterator_route(self, client):
        """Test iterator pattern route."""
        response = client.get("/pattern/behavioral/iterator")
        assert response.status_code == 200
        assert b"Iterator" in response.data

    def test_mediator_route(self, client):
        """Test mediator pattern route."""
        response = client.get("/pattern/behavioral/mediator")
        assert response.status_code == 200
        assert b"Mediator" in response.data

    def test_visitor_route(self, client):
        """Test visitor pattern route."""
        response = client.get("/pattern/behavioral/visitor")
        assert response.status_code == 200
        assert b"Visitor" in response.data

    def test_memento_route(self, client):
        """Test memento pattern route."""
        response = client.get("/pattern/behavioral/memento")
        assert response.status_code == 200
        assert b"Memento" in response.data

    def test_template_method_route(self, client):
        """Test template method pattern route."""
        response = client.get("/pattern/behavioral/template_method")
        assert response.status_code == 200
        assert b"Template Method" in response.data


class TestPatternRegistry:
    """Test cases for pattern registry."""

    def test_registry_has_all_patterns(self, app):
        """Test registry contains all 23 expected patterns."""
        from patterns import get_pattern_registry

        registry = get_pattern_registry()
        expected_patterns = [
            # Creational (5)
            "creational/abstract_factory",
            "creational/singleton",
            "creational/factory_method",
            "creational/builder",
            "creational/prototype",
            # Structural (7)
            "structural/adapter",
            "structural/bridge",
            "structural/composite",
            "structural/decorator",
            "structural/facade",
            "structural/flyweight",
            "structural/proxy",
            # Behavioral (11)
            "behavioral/chain_of_responsibility",
            "behavioral/command",
            "behavioral/interpreter",
            "behavioral/iterator",
            "behavioral/mediator",
            "behavioral/strategy",
            "behavioral/visitor",
            "behavioral/observer",
            "behavioral/state",
            "behavioral/memento",
            "behavioral/template_method",
        ]
        for pattern in expected_patterns:
            assert pattern in registry
        assert len(registry) == 23

    def test_registry_pattern_has_required_fields(self, app):
        """Test each pattern has required metadata."""
        from patterns import get_pattern_registry

        registry = get_pattern_registry()
        for path, pattern in registry.items():
            assert "category" in pattern
            assert "name" in pattern
            assert "description" in pattern
            assert "demo_func" in pattern
            assert callable(pattern["demo_func"])
