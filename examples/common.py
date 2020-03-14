#!/usr/bin/env python3

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from appconfigpy import ConfigItem, ConfigManager, DefaultDisplayStyle


app_config_mgr = ConfigManager(
    config_name="example",
    config_items=[
        ConfigItem(
            name="token",
            initial_value=None,
            prompt_text="API Token",
            default_display_style=DefaultDisplayStyle.PART_VISIBLE,
            required=True,
        ),
        ConfigItem(name="path", prompt_text="ABC Path", initial_value="."),
        ConfigItem(
            name="number", prompt_text="XYZ Number", initial_value="", value_type=int, required=True
        ),
    ],
)
