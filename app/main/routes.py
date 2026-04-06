"""Main application routes."""

from flask import Blueprint, render_template

from patterns import get_pattern_registry

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    """Render the home page with list of all patterns."""
    registry = get_pattern_registry()
    return render_template("index.html", patterns=registry)
