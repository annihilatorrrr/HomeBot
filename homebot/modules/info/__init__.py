"""HomeBot info module."""

from homebot.core.mdlintf import ModuleInterface, mdlbinder
from telegram.ext import CommandHandler

from homebot.modules.info.main import (
	info,
)

class InfoModule(ModuleInterface):
	name = "info"
	version = "1.0"
	handlers = [
		CommandHandler(["info"], info, run_async=True),
	]

mdlbinder.register_interface(InfoModule())
