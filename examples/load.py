#!/usr/bin/env python
# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import print_function, unicode_literals

import json

from common import app_config_mgr


print("loading configuration file path: {:s}".format(app_config_mgr.config_filepath))
print("configuration values: {}".format(json.dumps(app_config_mgr.load(), indent=4)))
