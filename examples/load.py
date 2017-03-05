#!/usr/bin/env python
# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import print_function
from __future__ import unicode_literals

from common import app_config_manager


if __name__ == "__main__":
    print(app_config_manager.load())
