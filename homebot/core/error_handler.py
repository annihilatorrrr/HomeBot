from homebot.core.config import get_config
from homebot.lib.libexception import format_exception
from homebot.lib.liblogging import LOGE
from telegram.ext import CallbackContext
from telegram.update import Update

LOGGING_CHAT_ID = get_config("bot.logging_chat_id")

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

	if LOGGING_CHAT_ID:
		try:
			context.bot.send_message(chat_id=LOGGING_CHAT_ID, text=formatted_error)
		except Exception as e:
			LOGE(f"Failed to send error to logging chat: {e}")

	LOGE("End error handling")
