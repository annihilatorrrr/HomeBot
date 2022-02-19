from datetime import datetime
from homebot.lib.libadmin import user_is_admin
from homebot.lib.liblineage.ota import get_nightlies
from homebot.modules.lineageos_updates.observer import Observer
from homebot.modules.lineageos_updates.poster import Poster
from telegram.bot import Bot
from telegram.ext import CallbackContext
from telegram.update import Update
from tempfile import TemporaryFile
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
	alive = _observer.thread.is_alive() and _observer.event.is_set()
	caption = (
		"Status:\n"
		f"Enabled: {str(alive)}\n"
	)
	text = ""
	if alive:
		caption += "List of devices:\n"
		text += (
			"Device | Last post\n"
		)
		for device in _observer.last_device_post:
			date = _observer.last_device_post[device]
			text += f"{device} | {date.strftime('%Y/%m/%d, %H:%M:%S')}\n"

	if text:
		fd = TemporaryFile(mode='r+')
		fd.write(text)
		fd.seek(0)
		update.message.reply_document(document=fd, filename="output.txt", caption=caption)
		fd.close()
	else:
		update.message.reply_text(caption)

def test_post(update: Update, context: CallbackContext):
	if len(context.args) < 2:
		update.message.reply_text("Error: No device provided")
		return

	device = context.args[1]
	chat_id = update.message.chat_id

	try:
		response = get_nightlies(device)
	except Exception:
		response = []

	if not response:
		update.message.reply_text(f"No updates for {device}")
		return

	last_update = response[-1]

	build_date = last_update.datetime

	for poster in _observer.posters.values():
		try:
			poster.post(device, last_update, chat_id)
		except Exception:
			pass
		else:
			update.message.reply_text(f"Build {device} {build_date} posted successfully")
			return

	update.message.reply_text(f"Error: Could not post {device} {build_date}")

def set_start_date(update: Update, context: CallbackContext):
	if len(context.args) < 2:
		update.message.reply_text("Error: No timestamp provided")
		return

	try:
		date = datetime.fromtimestamp(int(context.args[1]))
	except Exception:
		update.message.reply_text(f"Error: Invalid timestamp: {context.args[1]}")
		return

	_observer.set_start_date(date)

	update.message.reply_text(f"Start date set to {date.strftime('%Y/%m/%d, %H:%M:%S')}")

# name: function
COMMANDS: dict[str, Callable[[Update, CallbackContext], None]] = {
	"disable": disable,
	"enable": enable,
	"info": info,
	"set_start_date": set_start_date,
	"test_post": test_post,
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
