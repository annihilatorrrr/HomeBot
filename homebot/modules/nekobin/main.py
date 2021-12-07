from homebot.lib.libnekobin import to_nekobin
from io import BytesIO
from requests import HTTPError
from telegram.ext import CallbackContext
from telegram.update import Update

def nekobin(update: Update, context: CallbackContext):
	if not update.message.reply_to_message or not update.message.reply_to_message.document:
		update.message.reply_text("Usage: Reply /nekobin to a message containing a document")
		return

	document = update.message.reply_to_message.document
	message = update.message.reply_text("Uploading...")

	try:
		file: BytesIO = document.get_file().download(out=BytesIO())
	except Exception:
		message.edit_text("Error: failed to download file from Telegram (probably too big)")
		return

	text = file.getvalue().decode(encoding="utf-8", errors="ignore")

	try:
		url = to_nekobin(text)
	except HTTPError as e:
		message.edit_text(f"Error: failed to upload file to Nekobin: {e.response.status_code}")
	except Exception as e:
		message.edit_text(f"Error: failed to upload file to Nekobin: unknown error")
	else:
		message.edit_text(f"File uploaded to Nekobin: {url}", disable_web_page_preview=True)
	finally:
		file.close()
