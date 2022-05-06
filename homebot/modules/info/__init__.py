"""HomeBot info module."""

from homebot.core.mdlintf import ModuleInterface, mdlbinder
from telegram.botcommand import BotCommand
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
	commands_help = [
		BotCommand("info", "Get information about a message or a user or a chat"),
	]

mdlbinder.register_interface(InfoModule())
