from textwrap import dedent

import pytest

from appconfigpy import ConfigItem, ConfigManager, DefaultDisplayStyle


config_mgr = ConfigManager(
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
        ConfigItem(name="number", prompt_text="XYZ Number", initial_value="", value_type=int),
    ],
)


class Test_load:
    @pytest.mark.parametrize(
        ["value", "expected"],
        [
            [
                dedent(
                    """\
                    {
                        "token": "aaa",
                        "path": "bbb",
                        "number": 89
                    }
                    """
                ),
                {"number": 89, "path": "bbb", "token": "aaa"},
            ],
            [
                dedent(
                    """\
                    {
                        "token": "aaa",
                        "hogehoge": 89
                    }
                    """
                ),
                {"token": "aaa"},
            ],
            ['{ "token" : "aaa" }', {"token": "aaa"}],
        ],
    )
    def test_normal(self, tmpdir, value, expected):
        config_filepath = str(tmpdir.join(".config"))
        with open(config_filepath, "w") as f:
            f.write(value)
            f.flush()

        assert config_mgr.load(config_filepath) == expected

    @pytest.mark.parametrize(["value", "expected"], [["{}", ValueError]])
    def test_exception(self, tmpdir, value, expected):
        config_filepath = str(tmpdir.join(".config"))
        with open(config_filepath, "w") as f:
            f.write(value)
            f.flush()

        with pytest.raises(expected):
            config_mgr.load(config_filepath)
