from homebot.core.config import get_config
from homebot.modules.politically_correct.words import niceify
from telegram.ext import CallbackContext
from telegram.update import Update

ENABLE = get_config("politically_correct.enable", False)
CHAT_IDS = get_config("politically_correct.chat_ids", [])

def politically_correct(update: Update, context: CallbackContext):
	if not ENABLE:
		return

	if (update.effective_chat.username not in CHAT_IDS) and (update.effective_chat.id not in CHAT_IDS):
		return

	if not update.effective_message.text:
		return

	# Check if there's a bad word in the message
	niced_text = niceify(update.effective_message.text)

	if niced_text == update.effective_message.text:
		return

	if not update.effective_chat.get_member(context.bot.id).can_delete_messages:
		update.effective_message.reply_text("I can't delete messages in this chat.")

	user = update.effective_user
	user_description = f"{user.full_name} (@{user.username})" if user.username else user.full_name

	text = f"{user_description} said:\n"
	text += "\n"
	text += niced_text

	update.effective_message.delete()
	update.effective_chat.send_message(text)
