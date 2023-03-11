#!/usr/bin/env python3

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import json

from common import app_config_mgr


print(f"loading configuration file path: {app_config_mgr.config_filepath:s}")
print(f"configuration values: {json.dumps(app_config_mgr.load(), indent=4)}")
