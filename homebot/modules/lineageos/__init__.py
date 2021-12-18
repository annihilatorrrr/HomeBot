"""HomeBot LineageOS module."""

from homebot.core.mdlintf import ModuleInterface, mdlbinder
from telegram.ext import CommandHandler

from homebot.modules.lineageos.main import (
	lineageos,
)

class LineageosModule(ModuleInterface):
	name = "lineageos"
	version = "1.0"
	handlers = [
		CommandHandler(["lineageos"], lineageos),
	]

mdlbinder.register_interface(LineageosModule())
