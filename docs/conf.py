# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'agrtool'
copyright = '2025, Marianne Case Bezaire'
author = 'Marianne Case Bezaire'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

import os
import sys
sys.path.insert(0, os.path.abspath('../src'))


extensions = [
    'sphinx.ext.autodoc',  # Automatically generate docstrings
    'sphinx.ext.napoleon',  # Support for Google style docstrings
    'sphinx.ext.viewcode',  # Add links to source code
    'sphinx_rtd_theme',     # Read the Docs theme
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster' # 'sphinx_rtd_theme' # 'alabaster'
html_static_path = ['_static']

# If you want to add any custom styles, uncomment the following:
# html_static_path = ['_static']

# -- Options for autodoc -----------------------------------------------------

# Automatically document members (functions, classes) and modules
autodoc_default_flags = ['members', 'undoc-members', 'show-inheritance']

# -- Options for Napoleon ----------------------------------------------------

# Napoleon settings for Google-style docstrings
napoleon_google_docstring = True
napoleon_numpy_docstring = False

# -- Additional settings -----------------------------------------------------

# If you want to add more custom configurations for your documentation, you can do it here.
