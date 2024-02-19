# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Minetester'
copyright = '2023, EleutherAI'
author = 'EleutherAI'
release = '0.0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

templates_path = ['_templates']
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

import os
import sys
sys.path.insert(0, os.path.abspath('../minetester'))
# ...
extensions = [
    'sphinx.ext.autodoc',
    'sphinx_autodoc_typehints',
    'sphinx.ext.napoleon',
    'sphinx_rtd_theme',
    'sphinx.ext.viewcode',
    'sphinx_copybutton',
    'sphinx.ext.autosummary',
    'myst_parser',
]
# ...
napoleon_google_docstring = True
napoleon_numpy_docstring = False
autosummary_generate = True
autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "special-members": "__init__",
    "show-inheritance": True,
}
source_suffix = {
    ".rst": "restructuredtext",
    ".txt": "markdown",
    ".md": "markdown",
}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_title = "Minetester"
html_static_path = ['_static']