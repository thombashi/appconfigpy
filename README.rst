appconfigpy
===============

.. image:: https://badge.fury.io/py/appconfigpy.svg
    :target: https://badge.fury.io/py/appconfigpy

.. image:: https://img.shields.io/pypi/pyversions/appconfigpy.svg
    :target: https://pypi.python.org/pypi/appconfigpy


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
------------------------------------
.. code:: python

    # configure.py

    import appconfigpy

    app_config_manager = appconfigpy.ConfigManager(
        config_name="example",
        config_item_list=[
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
        ])

    try:
        app_config_manager.configure()
    except KeyboardInterrupt:
        print()


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
------------------------------------
.. code:: python

    # load.py

    import appconfigpy

    app_config_manager = appconfigpy.ConfigManager(
        config_name="example",
        config_item_list=[
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
        ])

    print(app_config_manager.load())

.. code::

    $ ./load.py
    {'token': 'abcdefghijklmn', 'path': '.'}


Dependencies
============
Python 2.7+ or 3.4+

- `logbook <http://logbook.readthedocs.io/en/stable/>`__
- `msgfy <https://github.com/thombashi/msgfy>`__
- `pathvalidate <https://github.com/thombashi/pathvalidate>`__
- `typepy <https://github.com/thombashi/typepy>`__

Optional Dependencies
------------------------------------
- `click <https://github.com/pallets/click>`__
