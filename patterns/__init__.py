"""Pattern registry - central registration of all 23 C++ design patterns."""

from patterns.creational.abstract_factory import demonstrate as abstract_factory_demo
from patterns.creational.singleton import demonstrate as singleton_demo
from patterns.creational.factory_method import demonstrate as factory_method_demo
from patterns.creational.builder import demonstrate as builder_demo
from patterns.creational.prototype import demonstrate as prototype_demo

from patterns.structural.adapter import demonstrate as adapter_demo
from patterns.structural.bridge import demonstrate as bridge_demo
from patterns.structural.composite import demonstrate as composite_demo
from patterns.structural.decorator import demonstrate as decorator_demo
from patterns.structural.facade import demonstrate as facade_demo
from patterns.structural.flyweight import demonstrate as flyweight_demo
from patterns.structural.proxy import demonstrate as proxy_demo

from patterns.behavioral.chain_of_responsibility import (
    demonstrate as chain_of_responsibility_demo,
)
from patterns.behavioral.command import demonstrate as command_demo
from patterns.behavioral.interpreter import demonstrate as interpreter_demo
from patterns.behavioral.iterator import demonstrate as iterator_demo
from patterns.behavioral.mediator import demonstrate as mediator_demo
from patterns.behavioral.strategy import demonstrate as strategy_demo
from patterns.behavioral.visitor import demonstrate as visitor_demo
from patterns.behavioral.observer import demonstrate as observer_demo
from patterns.behavioral.state import demonstrate as state_demo
from patterns.behavioral.memento import demonstrate as memento_demo
from patterns.behavioral.template_method import demonstrate as template_method_demo

# Pattern registry mapping category/pattern_name to demonstration function
_pattern_registry = {
    # Creational Patterns (5)
    "creational/abstract_factory": {
        "category": "Creational",
        "name": "Abstract Factory",
        "description": "Creates families of related objects without specifying concrete classes.",
        "demo_func": abstract_factory_demo,
    },
    "creational/singleton": {
        "category": "Creational",
        "name": "Singleton",
        "description": "Ensures a class has only one instance with global access point.",
        "demo_func": singleton_demo,
    },
    "creational/factory_method": {
        "category": "Creational",
        "name": "Factory Method",
        "description": "Delegates object creation to subclasses via a factory method.",
        "demo_func": factory_method_demo,
    },
    "creational/builder": {
        "category": "Creational",
        "name": "Builder",
        "description": "Separates construction of complex objects from their representation.",
        "demo_func": builder_demo,
    },
    "creational/prototype": {
        "category": "Creational",
        "name": "Prototype",
        "description": "Creates new objects by cloning existing prototype instances.",
        "demo_func": prototype_demo,
    },
    # Structural Patterns (7)
    "structural/adapter": {
        "category": "Structural",
        "name": "Adapter",
        "description": "Converts one interface to another that clients expect.",
        "demo_func": adapter_demo,
    },
    "structural/bridge": {
        "category": "Structural",
        "name": "Bridge",
        "description": "Decouples abstraction from implementation so both can vary independently.",
        "demo_func": bridge_demo,
    },
    "structural/composite": {
        "category": "Structural",
        "name": "Composite",
        "description": "Composes objects into tree structures for part-whole hierarchies.",
        "demo_func": composite_demo,
    },
    "structural/decorator": {
        "category": "Structural",
        "name": "Decorator",
        "description": "Attaches responsibilities to objects dynamically without subclassing.",
        "demo_func": decorator_demo,
    },
    "structural/facade": {
        "category": "Structural",
        "name": "Facade",
        "description": "Provides simplified interface to a complex subsystem.",
        "demo_func": facade_demo,
    },
    "structural/flyweight": {
        "category": "Structural",
        "name": "Flyweight",
        "description": "Shares data to minimize memory usage for many similar objects.",
        "demo_func": flyweight_demo,
    },
    "structural/proxy": {
        "category": "Structural",
        "name": "Proxy",
        "description": "Provides surrogate for controlling access to another object.",
        "demo_func": proxy_demo,
    },
    # Behavioral Patterns (11)
    "behavioral/chain_of_responsibility": {
        "category": "Behavioral",
        "name": "Chain of Responsibility",
        "description": "Passes requests along a chain of handlers until one processes it.",
        "demo_func": chain_of_responsibility_demo,
    },
    "behavioral/command": {
        "category": "Behavioral",
        "name": "Command",
        "description": "Encapsulates requests as objects for parameterization and undo.",
        "demo_func": command_demo,
    },
    "behavioral/interpreter": {
        "category": "Behavioral",
        "name": "Interpreter",
        "description": "Defines grammar representation and interpreter for a language.",
        "demo_func": interpreter_demo,
    },
    "behavioral/iterator": {
        "category": "Behavioral",
        "name": "Iterator",
        "description": "Accesses aggregate elements sequentially without exposing representation.",
        "demo_func": iterator_demo,
    },
    "behavioral/mediator": {
        "category": "Behavioral",
        "name": "Mediator",
        "description": "Encapsulates object interactions to prevent explicit references.",
        "demo_func": mediator_demo,
    },
    "behavioral/strategy": {
        "category": "Behavioral",
        "name": "Strategy",
        "description": "Defines interchangeable algorithm family for runtime selection.",
        "demo_func": strategy_demo,
    },
    "behavioral/visitor": {
        "category": "Behavioral",
        "name": "Visitor",
        "description": "Separates algorithms from object structure for extensible operations.",
        "demo_func": visitor_demo,
    },
    "behavioral/observer": {
        "category": "Behavioral",
        "name": "Observer",
        "description": "Defines one-to-many dependency for automatic state change notification.",
        "demo_func": observer_demo,
    },
    "behavioral/state": {
        "category": "Behavioral",
        "name": "State",
        "description": "Allows object to alter behavior when internal state changes.",
        "demo_func": state_demo,
    },
    "behavioral/memento": {
        "category": "Behavioral",
        "name": "Memento",
        "description": "Captures and externalizes object state for later restoration.",
        "demo_func": memento_demo,
    },
    "behavioral/template_method": {
        "category": "Behavioral",
        "name": "Template Method",
        "description": "Defines algorithm skeleton with deferrable steps to subclasses.",
        "demo_func": template_method_demo,
    },
}


def register_patterns(app):
    """Register pattern routes with the Flask application.

    Args:
        app: Flask application instance to register routes with.
    """
    for path, info in _pattern_registry.items():
        endpoint_name = f"pattern_{path.replace('/', '_')}"

        def make_route(pattern_info, endpoint):
            @app.route(f"/pattern/{path}", endpoint=endpoint)
            def pattern_route():
                output = pattern_info["demo_func"]()
                from flask import render_template
                from patterns import get_pattern_registry

                return render_template(
                    "pattern_detail.html",
                    pattern=pattern_info,
                    output=output,
                    patterns=get_pattern_registry(),
                )

            return pattern_route

        make_route(info, endpoint_name)


def get_pattern_registry():
    """Return the complete pattern registry.

    Returns:
        Dictionary of registered patterns.
    """
    return _pattern_registry
