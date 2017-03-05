appconfigpy
===============

.. image:: https://badge.fury.io/py/appconfigpy.svg
    :target: https://badge.fury.io/py/appconfigpy

.. image:: https://img.shields.io/pypi/pyversions/appconfigpy.svg
    :target: https://pypi.python.org/pypi/appconfigpy
   
.. image:: https://coveralls.io/repos/github/thombashi/appconfigpy/badge.svg?branch=master
    :target: https://coveralls.io/github/thombashi/appconfigpy?branch=master


Summary
=======
A Python library to create/load an application configuration file.


Installation
============

::

    pip install appconfigpy


Usage
=====

Create A Configuration File
==============================
.. code:: python
    
    # configure.py

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

    if __name__ == "__main__":
        app_config_manager = appconfigpy.ConfigManager(
            config_name=CONFIG_NAME, config_item_list=CONFIG_ITEM_LIST)

        app_config_manager.configure()


.. code::

    $ ./configure.py
    API Token: abcdefghijklmn
    Path [.]:
    $ cat ~/.example
    {
        "path": ".",
        "token": "abcdefghijklmn"
    }

Load A Configuration File
==============================
.. code:: python
    
    # load.py

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

    if __name__ == "__main__":
        app_config_manager = appconfigpy.ConfigManager(
            config_name=CONFIG_NAME, config_item_list=CONFIG_ITEM_LIST)

        print(app_config_manager.load())

.. code::

    $ ./load.py
    {'token': 'abcdefghijklmn', 'path': '.'}


Dependencies
============

Python 2.7+ or 3.3+

- `click <https://github.com/pallets/click>`__
- `logbook <http://logbook.readthedocs.io/en/stable/>`__
- `pathvalidate <https://github.com/thombashi/pathvalidate>`__
- `typepy <https://github.com/thombashi/typepy>`__

