.. contents:: **appconfigpy**
   :backlinks: top
   :local:


Summary
=======
A Python library to create/load an application configuration file.


.. image:: https://badge.fury.io/py/appconfigpy.svg
    :target: https://badge.fury.io/py/appconfigpy
    :alt: PyPI package version

.. image:: https://img.shields.io/pypi/pyversions/appconfigpy.svg
    :target: https://pypi.org/project/appconfigpy
    :alt: Supported Python versions


Installation
============
::

    pip install appconfigpy


Usage
=====

Create a configuration file from user inputs
-------------------------------------------------------
.. code:: python

    # configure.py

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
        ],
    )

    app_config_mgr.configure()


.. code::

    $ ./configure.py
    API Token: abcdefghijklmn
    ABC Path [.]:
    $ cat ~/.example
    {
        "path": ".",
        "token": "abcdefghijklmn"
    }

Load a configuration file
-------------------------------------------------------
.. code:: python

    # load.py

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
        ],
    )

    print(app_config_mgr.load())

.. code::

    $ ./load.py
    {'token': 'abcdefghijklmn', 'path': '.'}


Dependencies
============
Python 2.7+ or 3.4+

- `six <https://pypi.org/project/six/>`__

Optional Dependencies
------------------------------------
- `click <https://github.com/pallets/click>`__
- `logbook <https://logbook.readthedocs.io/en/stable/>`__
    - Logging using logbook if the package installed
- `pathvalidate <https://github.com/thombashi/pathvalidate>`__
- `simplejson <https://github.com/simplejson/simplejson>`__
- `typepy <https://github.com/thombashi/typepy>`__
