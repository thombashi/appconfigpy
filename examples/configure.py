#!/usr/bin/env python
# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import print_function

from common import app_config_manager


try:
    app_config_manager.configure()
except KeyboardInterrupt:
    print()
