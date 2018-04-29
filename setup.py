#!/usr/bin/env python
# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import unicode_literals

import io
import os.path
import sys

import setuptools


PROJECT_NAME = "appconfigpy"
REQUIREMENT_DIR = "requirements"
ENCODING = "utf8"


with io.open("README.rst", encoding=ENCODING) as fp:
    long_description = fp.read()

with io.open(os.path.join(
        REQUIREMENT_DIR, "requirements.txt"), encoding=ENCODING) as f:
    install_requires = [line.strip() for line in f if line.strip()]

SETUPTOOLS_REQUIRES = ["setuptools>=38.3.0"]

setuptools.setup(
    name=PROJECT_NAME,
    version="0.0.3",
    author="Tsuyoshi Hombashi",
    author_email="tsuyoshi.hombashi@gmail.com",
    url="https://github.com/thombashi/{:s}".format(PROJECT_NAME),
    license="MIT License",
    description=(
        "A Python library to create/load an application configuration file."),
    include_package_data=True,
    keywords=["configuration"],
    long_description=long_description,
    packages=setuptools.find_packages(exclude=["test*"]),

    install_requires=SETUPTOOLS_REQUIRES + install_requires,
    setup_requires=SETUPTOOLS_REQUIRES,
    tests_require=[],

    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ])
