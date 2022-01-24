"""HomeBot CI module."""

from homebot.core.mdlintf import ModuleInterface, mdlbinder
from telegram.botcommand import BotCommand
from telegram.ext import CommandHandler

from homebot.modules.ci.main import (
	ci,
)

class CiModule(ModuleInterface):
	name = "ci"
	version = "1.0"
	handlers = [
		CommandHandler(["ci"], ci, run_async=True),
	]
	commands_help = [
		BotCommand("ci", "Trigger a workflow or get information about the queue"),
	]

mdlbinder.register_interface(CiModule())
