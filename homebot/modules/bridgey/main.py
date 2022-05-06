from telegram.bot import Bot
from homebot.modules.bridgey.coordinator import Coordinator
from homebot.modules.bridgey.platforms.telegram import TelegramPlatform, posters
from telegram.ext import CallbackContext
from telegram.update import Update

def add_user(self, bot: Bot):
	posters.append(bot)

def remove_user(self, bot: Bot):
	if bot in posters:
		posters.remove(bot)

def handle_telegram_update(update: Update, context: CallbackContext):
	for pool in Coordinator.pools.values():
		for platform in pool.platforms.values():
			if not isinstance(platform, TelegramPlatform):
				continue

			if platform.chat_id != update.message.chat.id:
				continue

			platform.on_message(platform.message_to_generic(update.message), update.message.message_id)

def bridgey(update: Update, context: CallbackContext):
	reply = "Bridgey status:\n"
	reply += f"Enabled: {Coordinator.enabled}\n"

	if Coordinator.enabled:
		for pool_name, pool in Coordinator.pools.items():
			reply += f"\n{pool_name}:\n"
			for platform_name, platform in pool.platforms.items():
				reply += f"    {platform_name}: Running: {platform.running}\n"
			reply += "\n"

	update.message.reply_text(reply)
