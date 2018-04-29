#!/usr/bin/env python
# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import print_function, unicode_literals

import json

from common import app_config_manager


print("loading configuration file path: {:s}".format(app_config_manager.config_file_path))
print("configuration values: {}".format(json.dumps(app_config_manager.load(), indent=4)))
