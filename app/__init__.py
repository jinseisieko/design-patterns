"""Application factory pattern for creating Flask app instances."""

import os

from flask import Flask

from app.extensions import db
from config import config

from patterns import register_patterns
from app.main import main_bp


def create_app(config_name=None):
    """Create and configure a Flask application.

    Args:
        config_name: Configuration environment name. Defaults to 'default'.

    Returns:
        Configured Flask application instance.
    """
    if config_name is None:
        config_name = "default"

    # Get the project root directory
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    template_dir = os.path.join(base_dir, "templates")

    app = Flask(__name__, template_folder=template_dir)
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)

    # Register blueprints
    app.register_blueprint(main_bp)

    # Register pattern routes
    register_patterns(app)

    # Create database tables
    with app.app_context():
        db.create_all()

    return app
