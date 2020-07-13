import codecs
import os

from setuptools import find_packages, setup

PACKAGE_NAME = "jsdProject"
VERSION = "0.1.0"
AUTHOR = "Tim 7"
AUTHOR_EMAIL = "jsd2020tim7@gmail.com"
DESCRIPTION = "A domain-specific language for business data visualisation"
KEYWORDS = "textX DSL python domain specific languages document graphics"
LICENSE = "MIT"
URL = "https://github.com/KrsticM/jsd"
setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    url=URL,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    keywords=KEYWORDS,
    license=LICENSE,
    packages=find_packages(),
    include_package_data=True,
    package_data={"": ["*.tx"]},
    install_requires=["textx_ls_core"],
    entry_points={"textx_languages": ["documentV=grammar:visualiseDataLanguage"]},
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)