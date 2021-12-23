"""HomeBot bridgey module."""

from homebot.core.mdlintf import ModuleInterface, mdlbinder
from telegram.ext import CommandHandler, MessageHandler
from telegram.ext.filters import Filters

from homebot.modules.bridgey.main import (
	add_user,
	remove_user,
	bridgey,
	handle_telegram_update,
)

class BridgeyModule(ModuleInterface):
	name = "bridgey"
	version = "1.0"
	add_user = add_user
	remove_user = remove_user
	handlers = [
		CommandHandler(["bridgey"], bridgey, run_async=True),
		MessageHandler(Filters.update.message, handle_telegram_update, run_async=True),
	]

mdlbinder.register_interface(BridgeyModule())
