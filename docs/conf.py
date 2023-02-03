"""Sphinx configuration."""
project = "Wolt Summer Eng Assignment"
author = "Andrew Quinn"
copyright = "2023, Andrew Quinn"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "myst_parser",
]
autodoc_typehints = "description"
html_theme = "furo"
