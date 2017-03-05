#!/usr/bin/env python
# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
from __future__ import unicode_literals

import appconfigpy

CONFIG_NAME = "example"
CONFIG_ITEM_LIST = [
    appconfigpy.ConfigItem(
        name="token",
        initial_value=None,
        prompt_text="API Token",
        default_display_style=appconfigpy.DefaultDisplayStyle.PART_VISIBLE
    ),
    appconfigpy.ConfigItem(
        name="path",
        prompt_text="Path",
        initial_value=".",
    ),
]

app_config_manager = appconfigpy.ConfigManager(
    config_name=CONFIG_NAME, config_item_list=CONFIG_ITEM_LIST)
