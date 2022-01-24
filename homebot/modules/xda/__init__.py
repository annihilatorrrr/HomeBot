"""HomeBot XDA module."""

from homebot.core.mdlintf import ModuleInterface, mdlbinder
from telegram.botcommand import BotCommand
from telegram.ext import CommandHandler

from homebot.modules.xda.main import (
	xda,
)

class XdaModule(ModuleInterface):
	name = "xda"
	version = "1.0"
	handlers = [
		CommandHandler(["xda"], xda, run_async=True),
	]
	commands_help = [
		BotCommand("xda", "Let a general XDA user speak"),
	]

mdlbinder.register_interface(XdaModule())
