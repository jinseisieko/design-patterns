"""Tests for Factory Method pattern demonstration."""

from patterns.creational.factory_method import demonstrate


class TestDemonstrate:
    """Test cases for demonstrate function."""

    def test_demonstrate_returns_dict(self):
        """Test that demonstrate returns a dictionary."""
        output = demonstrate()
        assert isinstance(output, dict)

    def test_demonstrate_has_cpp_code(self):
        """Test that C++ code is present."""
        output = demonstrate()
        assert "cpp_code" in output
        assert "PaymentProcessor" in output["cpp_code"]

    def test_demonstrate_has_intent(self):
        """Test that intent is present."""
        output = demonstrate()
        assert "intent" in output

    def test_demonstrate_has_anti_pattern_warning(self):
        """Test anti-pattern warning is present."""
        output = demonstrate()
        assert "anti_pattern" in output
        assert "Complexity Overhead" in output["anti_pattern"]
