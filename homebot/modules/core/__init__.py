"""HomeBot core module."""

from homebot.core.mdlintf import ModuleInterface, mdlbinder
from telegram.ext import CommandHandler

from homebot.modules.core.main import (
	start,
	modules,
	enable,
	disable,
	restart,
	shutdown,
)

class CoreModule(ModuleInterface):
	name = "core"
	version = "1.0"
	core: True
	handlers = [
		CommandHandler(["start", "help"], start, run_async=True),
		CommandHandler(["modules"], modules, run_async=True),
		CommandHandler(["enable"], enable, run_async=True),
		CommandHandler(["disable"], disable, run_async=True),
		CommandHandler(["restart"], restart, run_async=True),
		CommandHandler(["shutdown"], shutdown, run_async=True),
	]

mdlbinder.register_interface(CoreModule())
