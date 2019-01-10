#!/usr/bin/env python
# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import unicode_literals

from appconfigpy import ConfigItem, ConfigManager, DefaultDisplayStyle


app_config_mgr = ConfigManager(
    config_name="example",
    config_item_list=[
        ConfigItem(
            name="token",
            initial_value=None,
            prompt_text="API Token",
            default_display_style=DefaultDisplayStyle.PART_VISIBLE,
        ),
        ConfigItem(name="path", prompt_text="ABC Path", initial_value="."),
        ConfigItem(name="number", prompt_text="XYZ Number", initial_value="", value_type=int),
    ],
)
