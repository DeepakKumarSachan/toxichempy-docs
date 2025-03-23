import os
import sys

# -- 📌 Path Setup ---------------------------------------------------------
# Dynamically determine the root directory of the project
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../"))

sys.path.insert(0, os.path.join(project_root, "src"))  # ✅ Ensure `src/` is in path

# sys.path.insert(0, project_root)  # Add root directory
sys.path.insert(0, os.path.join(project_root, "toxichempy"))  # Add toxichempy package

# -- 📌 Project Information ------------------------------------------------
project = "ToxiChemPy"
copyright = "2025, Deepak Kumar Sachan"
author = "Deepak Kumar Sachan"
release = "0.1.0"

# -- 📌 General Sphinx Configuration ----------------------------------------
extensions = [
    "sphinx.ext.autodoc",          # Generate documentation from docstrings
    "sphinx.ext.napoleon",         # Support for Google/NumPy-style docstrings
    "sphinx.ext.viewcode",         # Add links to source code
    "sphinx.ext.autosummary",      # Auto-generate summaries for modules
    "sphinx.ext.coverage",         # Report documentation coverage
    "sphinx.ext.todo",             # Allow TODOs in documentation
    "sphinx.ext.githubpages",      # Publish docs on GitHub Pages
    "sphinx_autodoc_typehints",    # Include type hints in documentation
    "myst_parser",                 # Enable Markdown support
    "sphinx_copybutton",           # Add copy buttons to code blocks
    "sphinx.ext.intersphinx",      # Link to external docs (e.g., Python API)
    "sphinx.ext.ifconfig",         # Conditional content inclusion
    "sphinx.ext.doctest",          # Test code snippets in documentation
]

# -- 📌 Autodoc Configuration ----------------------------------------------
autodoc_default_options = {
    "members": True,                # Include all members (functions, classes)
    "undoc-members": True,          # Include members without docstrings
    "show-inheritance": True,       # Show class inheritance
    "special-members": "__init__",  # Include special methods like __init__
    "exclude-members": "__weakref__",  # Exclude unnecessary built-in attributes
}
autosummary_generate = True  # Auto-generate .rst files for module documentation

# -- 📌 Napoleon (Google-Style & NumPy-Style Docstrings) -------------------
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False

# -- 📌 Intersphinx Configuration (External Docs) -------------------------
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    "pandas": ("https://pandas.pydata.org/pandas-docs/stable/", None),
    "scikit-learn": ("https://scikit-learn.org/stable/", None),
}

# -- 📌 TODO Extension Configuration --------------------------------------
todo_include_todos = True  # Enable TODOs in the documentation

# -- 📌 HTML Output Configuration -----------------------------------------
html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
# Load the custom JavaScript file
html_js_files = ["custom.js"]
html_show_sourcelink = False  # Hide "view source" links for cleaner UI
templates_path = ["_templates"]

html_theme_options = {
    "collapse_navigation": False,  # Prevents auto-collapsing menus
    "sticky_navigation": True,  # Sidebar stays fixed when scrolling
    "navigation_depth": 4,  # Limits sidebar depth
    "titles_only": False,  # Keeps all section titles visible
    "html_show_sphinx": False,

}

html_sidebars = {
    "**": [
        "globaltoc.html",  # Table of contents
        "relations.html",  # Next/Previous page links
        "searchbox.html",  # Search bar
        "custom_sidebar.html",  # Custom developer info
    ]
}

# -- 📌 Disable Numbering in Sidebar -------------------------------------
numfig = False
numfig_secnum_depth = 0

html_favicon = 'static/favicon.png'

