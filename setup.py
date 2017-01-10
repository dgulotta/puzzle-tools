#!/usr/bin/env python
VERSION = "0.1.0"

from setuptools import find_packages, setup

setup(
    name="puzzletools",
    version=VERSION,
    packages=find_packages(),
    install_requires=[
        'beautifulsoup4[lxml]',
        'unidecode'
    ],
)
