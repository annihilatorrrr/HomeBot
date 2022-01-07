"""HomeBot Politically correct module."""

from homebot.core.mdlintf import ModuleInterface, mdlbinder
from telegram.ext import MessageHandler
from telegram.ext.filters import Filters

from homebot.modules.politically_correct.main import (
	politically_correct,
)

class PoliticallyCorrectModule(ModuleInterface):
	name = "politically_correct"
	version = "1.0"
	handlers = [
		MessageHandler(Filters.update.message, politically_correct, run_async=True),
	]

mdlbinder.register_interface(PoliticallyCorrectModule())
