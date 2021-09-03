from calendar import day_name
from datetime import datetime
from homebot.modules.lineageos_updates.device_data import get_device_updates
from homebot.lib.libadmin import user_is_admin
from homebot.modules.lineageos_updates.observer import observer
from homebot.modules.lineageos_updates.poster import Poster, posters
from shutil import which
from subprocess import check_output
from telegram.bot import Bot
from telegram.ext import CallbackContext
from telegram.update import Update

ADMIN_COMMANDS = [
	"enable",
	"disable",
]

ALL_COMMANDS = [
	"last",
	"when",
	"info",
] + ADMIN_COMMANDS

def add_user(bot: Bot):
	posters[bot] = Poster(bot)

def remove_user(bot: Bot):
	if bot in posters:
		del posters[bot]

def lineageos_updates(update: Update, context: CallbackContext):
	if not context.args:
		update.message.reply_text("Error: No argument provided")
		return

	command = context.args[0]

	if command in ADMIN_COMMANDS:
		if not user_is_admin(update.message.from_user.id):
			update.message.reply_text("Error: You are not authorized to interact with LineageOS updater")
			return

	reply = ""

	# God I would've appreciated a case-switch here
	if command == "last":
		if len(context.args) < 2:
			reply = "Device codename not specified"

		device = context.args[1]
		response = get_device_updates(device)
		if not response:
			reply = f"Error: no updates found for {device}"
		else:
			last_update = response[-1]
			reply = (f"Last update for {device}:\n"
					f"Filename: {last_update['filename']}\n"
					f"Version: {last_update['version']}\n"
					f"Download: {last_update['url']}")
	elif command == "when":
		if len(context.args) < 2:
			reply = "Device codename not specified"
		elif which("python2") is None:
			reply = "Python 2.x isn't installed, it is required to get the random int"
		else:
			device = context.args[1]
			command = f'from random import Random; print(Random("{device}").randint(1, 7))'
			day_int = int(check_output(f"python2 -c '{command}'", shell=True))
			day = day_name[day_int - 1]
			reply = f"The next build for {device} will be on {day}"
	elif command == "info":
		alive = observer.thread.is_alive()
		reply = f"Enabled: {str(alive)}\n"
		if alive:
			reply += (
				"Observed devices:\n"
				"Device | Last post\n"
			)
			for device in observer.last_device_post:
				date = datetime.fromtimestamp(observer.last_device_post[device])
				reply += f"{device} | {date.strftime('%Y/%m/%d, %H:%M:%S')}\n"
	elif command == "enable":
		observer.event.set()
		reply = "Observer enabled"
	elif command == "disable":
		observer.event.clear()
		reply = "Observer disabled"
	else:
		if command != "help":
			reply = f"Error: Unknown command {command}\n\n"

		reply += "Available commands:\n"
		reply += "\n".join(ALL_COMMANDS)

	update.message.reply_text(reply)

	return
