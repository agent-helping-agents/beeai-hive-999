"""
Sphinx Documentation Configuration for BeeAI Hive 999
"""

import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.abspath(".."))

project = "BeeAI Hive 999"
copyright = f"{datetime.now().year}, BeeAI Contributors"
author = "BeeAI Team"

release = "1.0.0"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "sphinx.ext.todo",
    "sphinx.ext.coverage",
    "sphinx_rtd_theme",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

html_theme_options = {
    "navigation_depth": 4,
    "collapse_navigation": False,
    "sticky_navigation": True,
    "includehidden": True,
}

html_context = {
    "github_user": "beeai-org",
    "github_repo": "beeai-hive-999",
    "github_version": "main",
    "doc_path": "docs",
}

autoclass_content = "both"
autodoc_member_order = "bysource"

todo_include_todos = True

napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = True
