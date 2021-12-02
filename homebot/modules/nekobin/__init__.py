"""HomeBot Nekobin module."""

from homebot.core.mdlintf import ModuleInterface, mdlbinder
from telegram.ext import CommandHandler

from homebot.modules.nekobin.main import (
	nekobin,
)

class NekobinModule(ModuleInterface):
	name = "nekobin"
	version = "1.0"
	handlers = [
		CommandHandler(["nekobin"], nekobin, run_async=True),
	]

mdlbinder.register_interface(NekobinModule())
