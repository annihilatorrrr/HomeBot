from datetime import datetime
from homebot.lib.libadmin import user_is_admin
from homebot.modules.lineageos_updates.observer import Observer
from homebot.modules.lineageos_updates.poster import Poster
from telegram.bot import Bot
from telegram.ext import CallbackContext
from telegram.update import Update
from typing import Callable

_observer = Observer()

def add_user(self, bot: Bot):
	_observer.posters[bot] = Poster(bot)

def remove_user(self, bot: Bot):
	if bot in _observer.posters:
		del _observer.posters[bot]

def disable(update: Update, context: CallbackContext):
	_observer.event.clear()
	update.message.reply_text("Observer disabled")

def enable(update: Update, context: CallbackContext):
	_observer.event.set()
	update.message.reply_text("Observer enabled")

def info(update: Update, context: CallbackContext):
	alive = _observer.thread.is_alive()
	text = f"Enabled: {str(alive)}\n"
	if alive:
		text += (
			"Observed devices:\n"
			"Device | Last post\n"
		)
		for device in _observer.last_device_post:
			date = datetime.fromtimestamp(_observer.last_device_post[device])
			text += f"{device} | {date.strftime('%Y/%m/%d, %H:%M:%S')}\n"

	update.message.reply_text(text)

# name: function
COMMANDS: dict[str, Callable[[Update, CallbackContext], None]] = {
	"disable": disable,
	"enable": enable,
	"info": info,
}

HELP_TEXT = (
	"Available commands:\n" +
	"\n".join(COMMANDS.keys())
)

def lineageos_updates(update: Update, context: CallbackContext):
	if not user_is_admin(update.message.from_user.id):
		update.message.reply_text("Error: You are not authorized to use this command")
		return

	if not context.args:
		update.message.reply_text(
			"Error: No argument provided\n\n"
			f"{HELP_TEXT}"
		)
		return

	command = context.args[0]

	if command not in COMMANDS:
		update.message.reply_text(
			f"Error: Unknown command {command}\n\n"
			f"{HELP_TEXT}"
		)
		return

	func = COMMANDS[command]

	func(update, context)
