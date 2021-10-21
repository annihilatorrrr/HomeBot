How to write a module
=====================

Module location and format
--------------------------

In HomeBot, modules are stored in ``homebot/modules/``

They can either be a folder (``homebot/modules/*/__init__.py``) or a single file (``homebot/modules/*.py``), just like a Python module, but the former one is preferred to keep order

On bot's start, all the modules will be imported and ignored if they raise an error

After that, the bot instance is created and all the modules will be inizialized and stored in the bot's instance

Code
----

(For this example, we'll call the module ``foo``)

First of all, we'll create the following files: ``homebot/modules/foo/__init__.py`` and ``homebot/modules/foo/main.py`` 

All modules must have the following pattern:

``__init__.py``::

    """HomeBot foo module."""

    from homebot.core.mdlintf import (
        ModuleInterface,
        register_module,
    )

    from homebot.modules.foo.main import (
        foo,
    )

    @register_module
    class FooModule(ModuleInterface)
        name = "foo",
        version = "1.0",
        commands = {
            foo: ["foo"],
        },

``main.py``::

    from telegram.ext import CallbackContext
    from telegram.update import Update

    def foo(self, update: Update, context: CallbackContext):
        return update.message.reply_text("bar")

Description
-----------

* Import mdlintf related stuff
* Import module's functions from main.py
* Create a ModuleInterface instance and register it:

  * ``name``: The name of your module
  * ``version``: The version of your module
  * ``commands``: A list containing ModuleCommand instances: it's a dictionary containing the following things:

    * Key: Function executed when the command is triggered
    * Value: A list of commands name that the bot must answer to

So if we launch the bot with this module and we send ``/foo`` to the bot, the bot will execute ``foo()``

To know how you can use ``Update`` and ``CallbackContext``, please refer to python-telegram-bot documentation (`here <https://python-telegram-bot.readthedocs.io/en/stable/telegram.update.html>`__ and `here <https://python-telegram-bot.readthedocs.io/en/stable/telegram.ext.callbackcontext.html>`__)
