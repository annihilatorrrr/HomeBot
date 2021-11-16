from homebot.lib.libnekobin import to_nekobin
from io import BytesIO
from telegram.ext import CallbackContext
from telegram.update import Update

def nekobin(update: Update, context: CallbackContext):
	if not update.message.reply_to_message or not update.message.reply_to_message.document:
		update.message.reply_text("Usage: Reply /nekobin to a message containing a document")
		return

	document = update.message.reply_to_message.document

	try:
		file: BytesIO = document.get_file().download(out=BytesIO())
	except Exception:
		update.message.reply_text("Error: failed to download file from Telegram (probably too big)")
		return

	try:
		url = to_nekobin(file.getvalue())
	except Exception:
		update.message.reply_text("Error: failed to upload file to Nekobin")
	else:
		update.message.reply_text(f"File uploaded to Nekobin: {url}", disable_web_page_preview=True)
	finally:
		file.close()
