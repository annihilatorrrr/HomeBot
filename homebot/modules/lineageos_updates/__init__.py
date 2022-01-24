"""HomeBot LineageOS updates module."""

from homebot.core.mdlintf import ModuleInterface, mdlbinder
from telegram.botcommand import BotCommand
from telegram.ext import CommandHandler

from homebot.modules.lineageos_updates.main import (
	add_user,
	remove_user,
	lineageos_updates,
)

class LineageosUpdatesModule(ModuleInterface):
	name = "lineageos_updates"
	version = "1.0"
	add_user = add_user
	remove_user = remove_user
	handlers = [
		CommandHandler(["lineageos_updates"], lineageos_updates, run_async=True),
	]
	commands_help = [
		BotCommand("lineageos_updates", "Get information about the LineageOS updates poster"),
	]

mdlbinder.register_interface(LineageosUpdatesModule())
