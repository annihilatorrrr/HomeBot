"""HomeBot speedtest module."""

from homebot.core.mdlintf import ModuleInterface, mdlbinder
from telegram.botcommand import BotCommand
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
	commands_help = [
		BotCommand("speedtest", "Do a speedtest (will return the bot's machine Internet connection speed)"),
	]

mdlbinder.register_interface(SpeedtestModule())
