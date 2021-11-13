from telegram.bot import Bot
from homebot.modules.bridgey.coordinator import Coordinator
from homebot.modules.bridgey.platforms.telegram import TelegramPlatform, posters, CHAT_ID
from telegram.ext import CallbackContext
from telegram.update import Update

coordinator = Coordinator.DEFAULT
telegramplatform = coordinator.platforms[TelegramPlatform]

def add_user(self, bot: Bot):
	posters.append(bot)

def remove_user(self, bot: Bot):
	if bot in posters:
		posters.remove(bot)

def handle_telegram_update(update: Update, context: CallbackContext):
	if not telegramplatform.running:
		return

	if (update.message.chat.username != CHAT_ID) and (update.message.chat.id != CHAT_ID):
		return

	telegramplatform.on_message(telegramplatform.message_to_generic(update.message))

def bridgey(update: Update, context: CallbackContext):
	reply = "Bridgey status:"
	for platform in coordinator.platforms.values():
		reply += f"\n{platform.NAME}:\n"
		reply += f"Running: {platform.running}\n"

	update.message.reply_text(reply)
