"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import enum
import errno
import os.path
import sys
from dataclasses import dataclass
from typing import Any, Dict, List, Mapping, Optional, Sequence, Type, Union

from ._const import NULL_VALUE
from ._logger import logger


try:
    import simplejson as json  # type: ignore
except ImportError:
    import json


class DefaultDisplayStyle(enum.Enum):
    VISIBLE = "VISIBLE"
    PART_VISIBLE = "PART_VISIBLE"
    HIDDEN = "HIDDEN"


@dataclass(frozen=True)
class ConfigItem:
    name: str
    initial_value: Any
    value_type: Type = str
    prompt_text: str = ""
    default_display_style: DefaultDisplayStyle = DefaultDisplayStyle.VISIBLE
    required: bool = False

    @property
    def config_name(self) -> str:
        return self.name

    @property
    def show_default(self) -> bool:
        return self.default_display_style == DefaultDisplayStyle.VISIBLE

    def __post_init__(self) -> None:
        try:
            import typepy

            typepy.type.String(self.name).validate()
        except ImportError:
            pass

        if self.default_display_style not in DefaultDisplayStyle:
            raise ValueError(f"invalid display style: actual={self.default_display_style}")


class ConfigManager:
    @property
    def config_filepath(self) -> str:
        return self.__config_filepath

    @property
    def config_file_path(self):
        import warnings

        warnings.warn(
            "'config_file_path' property is deprecated and will be removed in the future."
            " use 'config_filepath' instead.",
            DeprecationWarning,
        )

        return self.__config_filepath

    @property
    def exists(self) -> bool:
        return os.path.exists(self.__config_filepath)

    def __init__(self, config_name: str, config_items: Sequence[ConfigItem]) -> None:
        try:
            import pathvalidate

            pathvalidate.validate_filename(config_name)
        except ImportError:
            pass

        self.__logger = logger
        self.__config_filepath = os.path.normpath(
            os.path.expanduser(os.path.join("~", ".{:s}".format(config_name.lstrip("."))))
        )
        self.__config_items = config_items

    def load(
        self, config_filepath: Optional[str] = None
    ) -> Dict[str, Union[int, float, str, None]]:
        if not config_filepath:
            config_filepath = self.config_filepath

        if not os.path.isfile(config_filepath):
            self.__logger.debug(f"config file not found: path='{config_filepath}'")
            return {}

        with open(config_filepath) as f:
            loaded_configs = json.load(f)

        self.__logger.debug(
            f"config file loaded: path='{config_filepath}', entries={len(loaded_configs)}"
        )

        valid_configs: Dict[str, Union[int, float, str, None]] = {}
        invalid_configs: List[str] = []

        for config_item in self.__config_items:
            if config_item.config_name not in loaded_configs:
                if config_item.required:
                    invalid_configs.append(config_item.config_name)

                continue

            valid_configs[config_item.config_name] = loaded_configs.get(config_item.config_name)

        self.__logger.debug(
            f"valid loaded configurations: {len(valid_configs)}/{len(loaded_configs)}"
        )

        if invalid_configs:
            raise ValueError("required configs not found: {}".format("".join(invalid_configs)))

        return valid_configs

    def configure(self) -> int:
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
                prompt_text += " [{}]".format("*" * 10 + str(old_value)[-4:])

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

        self.__logger.debug(f"written {len(self.__config_items)} configurations")

        return self.__write_config(new_config)

    def __prompt_value_click(
        self, prompt_text: str, current_value: Any, config_item: ConfigItem
    ) -> Any:
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

    def __prompt_value_builtin(
        self, prompt_text: str, current_value: Any, config_item: ConfigItem
    ) -> Any:
        if config_item.show_default:
            prompt_text = f"{prompt_text:s} [{current_value}]: "
        else:
            prompt_text = f"{prompt_text:s}: "

        return config_item.value_type(input(prompt_text))

    def __prompt_value(self, prompt_text: str, current_value: Any, config_item: ConfigItem) -> Any:
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
                sys.stderr.write(f"Error: {new_value} is not a valid {config_item.value_type}\n")

        return new_value

    def __write_config(self, config: Mapping[str, Any]) -> int:
        try:
            with open(self.config_filepath, "w", encoding="utf8") as f:
                f.write(json.dumps(config, indent=4, ensure_ascii=False) + "\n")
        except OSError as e:
            self.__logger.error(e)

            return e.args[0]

        self.__logger.debug(f"written configurations to '{self.config_filepath:s}'")

        return 0
