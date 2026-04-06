"""Tests for Singleton pattern demonstration."""

from patterns.creational.singleton import demonstrate


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
        assert "getInstance()" in output["cpp_code"]

    def test_demonstrate_has_before_after(self):
        """Test that before/after code is present."""
        output = demonstrate()
        assert "before_code" in output
        assert "after_code" in output

    def test_demonstrate_has_intent(self):
        """Test that intent is present."""
        output = demonstrate()
        assert "intent" in output
        assert "one instance" in output["intent"].lower()

    def test_demonstrate_has_anti_pattern_warning(self):
        """Test anti-pattern warning is present."""
        output = demonstrate()
        assert "anti_pattern" in output
        assert "God Object" in output["anti_pattern"]

    def test_demonstrate_has_uml_diagram(self):
        """Test that UML diagram is present."""
        output = demonstrate()
        assert "uml_diagram" in output
