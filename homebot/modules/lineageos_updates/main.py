from calendar import day_name
from datetime import datetime
from homebot.lib.libadmin import user_is_admin
from homebot.modules.lineageos_updates.observer import observer
from homebot.modules.lineageos_updates.poster import Poster, posters
from shutil import which
from subprocess import check_output
from telegram.bot import Bot
from telegram.ext import CallbackContext
from telegram.update import Update

def add_user(bot: Bot):
	posters[bot] = Poster(bot)

def remove_user(bot: Bot):
	if bot in posters:
		del posters[bot]

def lineageos_updater(update: Update, context: CallbackContext):
	if not user_is_admin(update.message.from_user.id):
		update.message.reply_text("Error: You are not authorized to interact with LineageOS updater")
		return

	if not context.args:
		update.message.reply_text("Error: No argument provided")
		return	

	command = context.args[0]

	if command == "when":
		if len(context.args) < 2:
			reply = f"Device codename not specified"
		elif which("python2") is None:
			reply = f"Python 2.x isn't installed, it is required to get the random int"
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
				f"Observed devices:\n"
				f"\n"
				f"Device | Last update\n"
			)
			for device in observer.last_device_update:
				date = datetime.fromtimestamp(observer.last_device_update[device])
				reply += f"{device} | {date.year}/{date.month}/{date.day}\n"
	elif command == "enable":
		observer.event.set()
		reply = "Observer enabled"
	elif command == "disable":
		observer.event.clear()
		reply = "Observer disabled"
	else:
		reply = "Error: Unknown command"

	update.message.reply_text(reply)

	return
