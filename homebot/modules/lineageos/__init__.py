"""HomeBot LineageOS module."""

from homebot.core.mdlintf import ModuleInterface, mdlbinder
from telegram.botcommand import BotCommand
from telegram.ext import CommandHandler

from homebot.modules.lineageos.main import (
	lineageos,
)

class LineageosModule(ModuleInterface):
	name = "lineageos"
	version = "1.0"
	handlers = [
		CommandHandler(["lineageos"], lineageos, run_async=True),
	]
	commands_help = [
		BotCommand("lineageos", "LineageOS OTA and wiki utils"),
	]

mdlbinder.register_interface(LineageosModule())
