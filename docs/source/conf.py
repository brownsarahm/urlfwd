# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'urlfwd'
copyright = '2025, Sarah M Brown'
author = 'Sarah M Brown'
release = '0.3'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration


# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "myst_nb",
    'sphinx.ext.intersphinx',
    "sphinx_design",
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx_click'
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', "*import_posts*",
        "**/pandoc_ipynb/inputs/*", ".nox/*", "README.md",]



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output


# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'pydata_sphinx_theme'


html_theme_options = {
  "show_nav_level": 1,
  "header_links_before_dropdown": 6,
  "icon_links": [ 
        {
            "name": "Source on GitHub",
            "url": "https://github.com/brownsarahm/urlwd",
            "icon": "fa-brands fa-github",
        },
        {
            "name": "Author",
            "url": "https://github.com/brownsarahm",
            "icon": "fa-solid fa-user",
        },
        {
            "name": "Example Usage",
            "url": "https://drsmb.co",
            "icon": "fa-solid fa-link",
        },
        {
            "name": "Example Source",
            "url": "https://github.com/drsmb-co/drsmb-co.github.io",
            "icon": "fa-solid fa-code",
        }],
  "secondary_sidebar_items": {
        "**/*": ["page-toc", "edit-this-page", "sourcelink"],
    }
}

# html_favicon = "_static/favicon.ico"
#  change this to change the site title
html_title = project

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
# html_extra_path = ["feed.xml"]
# map pages to which sidebar they should have
#  "page_file_name": ["list.html", "of.html", "sidebar.html", "files.html"]
html_sidebars = {
    "*": [],
    "**/*": ["sidebar-nav-bs",]
}



# Panels config
panels_add_bootstrap_css = False

# MyST config
myst_enable_extensions = [
    # "amsmath",
    "colon_fence",
    "deflist",
    "dollarmath",
    "fieldlist",
    "html_admonition",
    "html_image",
    # "linkify",
    "replacements",
    "smartquotes",
    "strikethrough",
    "substitution",
    # "tasklist",
]