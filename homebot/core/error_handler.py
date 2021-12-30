from homebot.core.config import get_config
from homebot.lib.libexception import format_exception
from homebot.lib.liblogging import LOGE
from telegram.bot import Bot
from telegram.ext import CallbackContext
from telegram.update import Update

LOGGING_CHAT_ID = get_config("bot.logging_chat_id")

def log_to_logging_chat(bot: Bot, text: str):
	"""Send a message to the logging chat.

	Returns True if the message was sent successfully, False otherwise."""
	if not LOGGING_CHAT_ID:
		return False

	try:
		bot.send_message(chat_id=LOGGING_CHAT_ID, text=text)
	except Exception as e:
		LOGE(f"Failed to send message to logging chat: {e}")
		return False
	else:
		return True

def error_handler(update: Update, context: CallbackContext):
	formatted_error = "HomeBot: Error encountered!\n"
	if update.effective_chat:
		formatted_error += f"Chat: {update.effective_chat.full_name} {f'(@{update.effective_chat.username})' if update.effective_chat.username else f'{update.effective_chat.id}'}\n"
	if update.effective_user:
		formatted_error += f"User: {update.effective_user.full_name} {f'(@{update.effective_user.username})' if update.effective_user.username else f'{update.effective_user.id}'}\n"
	if update.effective_message:
		formatted_error += f"Message: {update.effective_message.text}\n"
	formatted_error += f"\n{format_exception(context.error)}"

	LOGE(formatted_error)

	log_to_logging_chat(context.bot, formatted_error)

	LOGE("End error handling")
