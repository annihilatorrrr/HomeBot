from homebot.lib.libadmin import user_is_admin
from homebot.modules.lineageos_updates.observer import observer
from homebot.modules.lineageos_updates.poster import Poster, posters
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

	if command == "enable":
		observer.event.set()
		update.message.reply_text("Observer enabled")
	elif command == "disable":
		observer.event.clear()
		update.message.reply_text("Observer disabled")
	else:
		update.message.reply_text("Error: Unknown command")

	return
