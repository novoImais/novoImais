import os
import sys

sys.path.insert(0, os.path.abspath("../.."))

# -- Project information -----------------------------------------------------

project = "xml-reader-producer"
copyright = "2021, Luan Moreno"
author = "Luan Moreno"
release = "1.0.6"

# -- General configuration ---------------------------------------------------
extensions = [
    "sphinx.ext.napoleon",
    "pallets_sphinx_themes",
    "sphinx.ext.autodoc",
    "rinoh.frontend.sphinx",
]
templates_path = ["_templates"]


# -- HTML output -------------------------------------------------
html_theme = "flask"
html_static_path = ["_static"]

# -- Additional configuration ---------------------------------------------------
napoleon_use_ivar = True
napoleon_google_docstring = True