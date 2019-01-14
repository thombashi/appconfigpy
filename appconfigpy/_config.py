# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import, unicode_literals

import errno
import io
import os.path
import sys

import six

from ._const import NULL_VALUE
from ._logger import logger


try:
    import simplejson as json
except ImportError:
    import json


class DefaultDisplayStyle(object):
    VISIBLE = "VISIBLE"
    PART_VISIBLE = "PART_VISIBLE"
    HIDDEN = "HIDDEN"

    LIST = [VISIBLE, PART_VISIBLE, HIDDEN]


class ConfigItem(object):
    @property
    def show_default(self):
        return self.default_display_style == DefaultDisplayStyle.VISIBLE

    def __init__(
        self,
        name,
        initial_value,
        value_type=str,
        prompt_text=None,
        default_display_style=DefaultDisplayStyle.VISIBLE,
        required=False,
    ):
        try:
            import typepy

            typepy.type.String(name).validate()
        except ImportError:
            pass

        if default_display_style not in DefaultDisplayStyle.LIST:
            raise ValueError(
                "invalid style: expected={}, actual={}".format(
                    DefaultDisplayStyle.LIST, default_display_style
                )
            )

        self.config_name = name
        self.value_type = value_type
        self.initial_value = initial_value
        self.prompt_text = prompt_text if prompt_text else name
        self.default_display_style = default_display_style
        self.required = required


class ConfigManager(object):
    @property
    def config_filepath(self):
        return self.__config_filepath

    @property
    def config_file_path(self):
        return self.__config_filepath

    @property
    def exists(self):
        return os.path.exists(self.__config_filepath)

    def __init__(self, config_name, config_item_list):
        try:
            import pathvalidate

            pathvalidate.validate_filename(config_name)
        except ImportError:
            pass

        self.__logger = logger
        self.__config_filepath = os.path.normpath(
            os.path.expanduser(os.path.join("~", ".{:s}".format(config_name.lstrip("."))))
        )
        self.__config_items = config_item_list

    def load(self, config_filepath=None):
        if not config_filepath:
            config_filepath = self.config_filepath

        if not os.path.isfile(config_filepath):
            self.__logger.debug("config file not found: path='{}'".format(config_filepath))
            return {}

        with open(config_filepath) as f:
            loaded_configs = json.load(f)

        self.__logger.debug(
            "config file loaded: path='{}', entries={}".format(config_filepath, len(loaded_configs))
        )

        valid_configs = {}
        invalid_configs = []

        for config_item in self.__config_items:
            if config_item.config_name not in loaded_configs:
                if config_item.required:
                    invalid_configs.append(config_item.config_name)

                continue

            valid_configs[config_item.config_name] = loaded_configs.get(config_item.config_name)

        self.__logger.debug(
            "valid loaded configurations: {}/{}".format(len(valid_configs), len(loaded_configs))
        )

        if invalid_configs:
            raise ValueError("required configs not found: {}".format("".join(invalid_configs)))

        return valid_configs

    def configure(self):
        old_config = self.load()
        new_config = {}

        for config_item in self.__config_items:
            old_value = old_config.get(config_item.config_name, config_item.initial_value)
            prompt_text = config_item.prompt_text

            if config_item.required:
                prompt_text += " (required)"

            if all(
                [
                    old_value,
                    old_value != NULL_VALUE,
                    config_item.default_display_style == DefaultDisplayStyle.PART_VISIBLE,
                ]
            ):
                prompt_text += " [{}]".format("*" * 10 + six.text_type(old_value)[-4:])

            try:
                while True:
                    new_value = self.__prompt_value(prompt_text, old_value, config_item)
                    new_config[config_item.config_name] = new_value

                    if not config_item.required:
                        break

                    if new_value:
                        break
            except KeyboardInterrupt:
                self.__logger.debug("keyboard interrupt")
                return errno.EINTR

        self.__logger.debug("written {} configurations".format(len(self.__config_items)))

        return self.__write_config(new_config)

    def __prompt_value_click(self, prompt_text, current_value, config_item):
        import click

        try:
            return click.prompt(
                prompt_text,
                type=config_item.value_type,
                default=current_value,
                show_default=config_item.show_default,
            )
        except click.exceptions.Abort:
            raise KeyboardInterrupt()

    def __prompt_value_builtin(self, prompt_text, current_value, config_item):
        from six.moves import input

        if config_item.show_default:
            prompt_text = "{:s} [{}]: ".format(prompt_text, current_value)
        else:
            prompt_text = "{:s}: ".format(prompt_text)

        return config_item.value_type(input(prompt_text))

    def __prompt_value(self, prompt_text, current_value, config_item):
        try:
            return self.__prompt_value_click(prompt_text, current_value, config_item)
        except ImportError:
            pass

        is_valid_value = False
        new_value = None
        while not is_valid_value:
            try:
                new_value = self.__prompt_value_builtin(prompt_text, current_value, config_item)
                is_valid_value = True
            except (TypeError, ValueError):
                sys.stderr.write(
                    "Error: {} is not a valid {}\n".format(new_value, config_item.value_type)
                )

        return new_value

    def __write_config(self, config):
        try:
            with io.open(self.config_filepath, "w", encoding="utf8") as f:
                f.write(json.dumps(config, indent=4, ensure_ascii=False) + "\n")
        except IOError as e:
            self.__logger.error(e)

            return e.args[0]

        self.__logger.debug("written configurations to '{:s}'".format(self.config_filepath))

        return 0
