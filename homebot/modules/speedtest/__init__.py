"""HomeBot speedtest module."""

from homebot.core.mdlintf import ModuleInterface, mdlbinder
from telegram.ext import CommandHandler

from homebot.modules.speedtest.main import (
	speedtest,
)

class SpeedtestModule(ModuleInterface):
	name = "speedtest"
	version = "1.0"
	handlers = [
		CommandHandler(["speedtest"], speedtest, run_async=True),
	]

mdlbinder.register_interface(SpeedtestModule())
