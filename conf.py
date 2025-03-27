import os
import sys
import re
import sphinx_rtd_theme

# -- Path setup --------------------------------------------------------------
# Add your project's root directory to the sys.path so that Sphinx can find your modules.
sys.path.insert(0, os.path.abspath('../'))

# -- Project information -----------------------------------------------------

project = 'Autograder Tools'
copyright = '2025, Marianne Case Bezaire'
author = 'Marianne Case Bezaire'

# The full version, including alpha/beta/rc tags.
release = '0.1.0'  # You can automate this by extracting it from your project version, like in a version file.

# -- General configuration ---------------------------------------------------

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = 'Autograder Tools'
copyright = '2025, Marianne Case Bezaire'
author = 'Marianne Case Bezaire'

# -- Sphinx extensions ------------------------------------------------------

# Extensions to enable
extensions = [
    'sphinx.ext.autodoc',  # Automatically generate docstrings
    'sphinx.ext.napoleon',  # Support for Google style docstrings
    'sphinx.ext.viewcode',  # Add links to source code
    'sphinx_rtd_theme',     # Read the Docs theme
]

# -- Options for HTML output -------------------------------------------------

# Use Read the Docs' default theme
html_theme = 'sphinx_rtd_theme'

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
