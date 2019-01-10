# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import, unicode_literals


try:
    import logbook

    LOGBOOK_INSTALLED = True

    logger = logbook.Logger("appconfigpy")
    logger.disable()
except ImportError:
    LOGBOOK_INSTALLED = False

    class DummyLogger(object):
        def debug(self, *args, **kwargs):
            pass

        def error(self, *args, **kwargs):
            pass

    logger = DummyLogger()


def set_logger(is_enable):
    if not LOGBOOK_INSTALLED:
        return

    if is_enable:
        logger.enable()
    else:
        logger.disable()


def set_log_level(log_level):
    """
    Set logging level of this module. Using
    `logbook <https://logbook.readthedocs.io/en/stable/>`__ module for logging.

    :param int log_level:
        One of the log level of
        `logbook <https://logbook.readthedocs.io/en/stable/api/base.html>`__.
        Disabled logging if ``log_level`` is ``logbook.NOTSET``.
    """

    if not LOGBOOK_INSTALLED:
        return

    if log_level == logbook.NOTSET:
        set_logger(is_enable=False)
    else:
        set_logger(is_enable=True)

    logger.level = log_level
