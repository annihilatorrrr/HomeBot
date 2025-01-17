"""HomeBot shell module."""

from homebot.core.mdlintf import ModuleInterface, mdlbinder
from telegram.botcommand import BotCommand
from telegram.ext import CommandHandler

from homebot.modules.shell.main import (
	shell,
)

class ShellModule(ModuleInterface):
	name = "shell"
	version = "1.0"
	core: True
	handlers = [
		CommandHandler(["shell"], shell, run_async=True),
	]
	commands_help = [
		BotCommand("shell", "Execute a command in the bot's environment"),
	]

mdlbinder.register_interface(ShellModule())
