"""
Super Claude Plugins
--------------------
Drop-in plugin modules for extending the agent council.
Each plugin exports a `run(args)` function.
"""

import importlib
import os
import pkgutil


def list_plugins():
    """List all available plugins."""
    plugin_dir = os.path.dirname(__file__)
    plugins = []
    for _, name, _ in pkgutil.iter_modules([plugin_dir]):
        if name != "__init__":
            plugins.append(name)
    return plugins


def load_plugin(name):
    """Load and return a plugin module by name."""
    return importlib.import_module(f"plugins.{name}")


def run_plugin(name, args=None):
    """Load and run a plugin."""
    mod = load_plugin(name)
    return mod.run(args or {})
