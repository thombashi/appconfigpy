#!/usr/bin/env python
# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import print_function

from common import app_config_mgr


try:
    # input configurations are written to ~/.example
    app_config_mgr.configure()
except KeyboardInterrupt:
    print()
