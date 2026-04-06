"""Tests for Command pattern demonstration."""

from patterns.behavioral.command import demonstrate


class TestDemonstrate:
    """Test cases for demonstrate function."""

    def test_demonstrate_returns_dict(self):
        output = demonstrate()
        assert isinstance(output, dict)

    def test_demonstrate_has_cpp_code(self):
        output = demonstrate()
        assert "cpp_code" in output
        assert "Command" in output["cpp_code"]

    def test_demonstrate_has_intent(self):
        output = demonstrate()
        assert "intent" in output

    def test_demonstrate_has_anti_pattern_warning(self):
        output = demonstrate()
        assert "anti_pattern" in output
