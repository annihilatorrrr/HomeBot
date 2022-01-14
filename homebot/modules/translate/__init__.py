"""HomeBot speedtest module."""

from homebot.core.mdlintf import ModuleInterface, mdlbinder
from telegram.ext import CommandHandler

from homebot.modules.translate.main import (
	translate,
)

class TranslateModule(ModuleInterface):
	name = "translate"
	version = "1.0"
	handlers = [
		CommandHandler(["translate"], translate, run_async=True),
	]

mdlbinder.register_interface(TranslateModule())
