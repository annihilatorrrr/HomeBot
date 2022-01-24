"""HomeBot core module."""

from homebot.core.mdlintf import ModuleInterface, mdlbinder
from telegram.botcommand import BotCommand
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
	commands_help = [
		BotCommand("start", "Bot start point"),
		BotCommand("help", "Get help about the bot"),
		BotCommand("modules", "List of modules"),
		BotCommand("enable", "Enable a module"),
		BotCommand("disable", "Disable a module"),
		BotCommand("restart", "Restart the bot"),
		BotCommand("shutdown", "Shutdown the bot"),
	]

mdlbinder.register_interface(CoreModule())
