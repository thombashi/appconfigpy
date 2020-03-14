"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import pytest

from appconfigpy import set_logger
from appconfigpy._logger import NullLogger


class Test_set_logger:
    @pytest.mark.parametrize(["value"], [[True], [False]])
    def test_smoke(self, value):
        set_logger(value)


class Test_NullLogger:
    @pytest.mark.parametrize(["value"], [[True], [False]])
    def test_smoke(self, value, monkeypatch):
        monkeypatch.setattr("appconfigpy._logger", NullLogger())
        set_logger(value)
