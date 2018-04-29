# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import, unicode_literals

import io
import json
import os.path
import sys

import msgfy
import pathvalidate
import six
import typepy

from ._const import NULL_VALUE
from ._logger import logger


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
            self, name, initial_value, value_type=str, prompt_text=None,
            default_display_style=DefaultDisplayStyle.VISIBLE):
        typepy.type.String(name).validate()

        if default_display_style not in DefaultDisplayStyle.LIST:
            raise ValueError("invalid style: expected={}, actual={}".format(
                DefaultDisplayStyle.LIST, default_display_style))

        self.config_name = name
        self.value_type = value_type
        self.initial_value = initial_value
        self.prompt_text = prompt_text if prompt_text else name
        self.default_display_style = default_display_style


class ConfigManager(object):

    @property
    def config_file_path(self):
        return self.__config_file_path

    @property
    def exists(self):
        return os.path.exists(self.__config_file_path)

    def __init__(self, config_name, config_item_list):
        pathvalidate.validate_filename(config_name)

        self.__logger = logger
        self.__config_file_path = os.path.expanduser(
            os.path.join("~", ".{:s}".format(config_name)))
        self.__config_item_list = config_item_list

    def load(self):
        if not os.path.isfile(self.config_file_path):
            self.__logger.debug(
                "configuration file not found: path='{}'".format(self.config_file_path))
            return {}

        with open(self.config_file_path) as f:
            try:
                loaded_config = json.load(f)
            except ValueError as e:
                self.__logger.debug(msgfy.to_debug_message(e))
                return {}

        self.__logger.debug(
            "configuration file found: path='{}', loaded-entries={}".format(
                self.config_file_path, len(loaded_config)))

        valid_config = {}
        for config_item in self.__config_item_list:
            if config_item.config_name not in loaded_config:
                continue

            valid_config[config_item.config_name] = loaded_config.get(
                config_item.config_name)

        self.__logger.debug("valid loaded configurations: {}".format(len(valid_config)))

        return valid_config

    def configure(self):
        old_config = self.load()
        new_config = {}

        for config_item in self.__config_item_list:
            old_value = old_config.get(config_item.config_name, config_item.initial_value)
            prompt_text = config_item.prompt_text
            if all([
                old_value,
                old_value != NULL_VALUE,
                config_item.default_display_style == DefaultDisplayStyle.PART_VISIBLE
            ]):
                prompt_text += " [{}]".format("*" * 10 + six.text_type(old_value)[-4:])

            new_config[config_item.config_name] = self.__prompt_value(
                prompt_text, old_value, config_item)

        self.__logger.debug("written {} configurations".format(len(self.__config_item_list)))

        return self.__write_config(new_config)

    def __prompt_value_click(self, prompt_text, current_value, config_item):
        import click

        try:
            return click.prompt(
                prompt_text, type=config_item.value_type,
                default=current_value, show_default=config_item.show_default)
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
                sys.stderr.write("Error: {} is not a valid {}\n".format(
                    new_value, config_item.value_type))

        return new_value

    def __write_config(self, config):
        try:
            with io.open(self.config_file_path, "w", encoding="utf8") as f:
                f.write(json.dumps(config, indent=4, ensure_ascii=False) + "\n")
        except IOError as e:
            self.__logger.error(msgfy.to_error_message(e))
            return e.args[0]

        self.__logger.debug("written configurations to '{:s}'".format(self.config_file_path))

        return 0
