from io import BytesIO
from requests import HTTPError
from sebaubuntu_libs.libnekobin import to_nekobin
from telegram.ext import CallbackContext
from telegram.update import Update

def nekobin(update: Update, context: CallbackContext):
	reply_to_message = update.message.reply_to_message

	if not reply_to_message:
		update.message.reply_text("Usage: Reply /nekobin to a message")
		return

	if not reply_to_message.document and not reply_to_message.text:
		update.message.reply_text("Usage: Reply /nekobin to a message containing a document or text")
		return

	message = update.message.reply_text("Uploading...")

	if reply_to_message.document:
		try:
			with reply_to_message.document.get_file().download(out=BytesIO()) as f:
				text = f.getvalue().decode(encoding="utf-8", errors="ignore")
		except Exception:
			message.edit_text("Error: failed to download file from Telegram (probably too big)")
			return
	else:
		text = reply_to_message.text

	try:
		url = to_nekobin(text)
	except HTTPError as e:
		message.edit_text(f"Error: failed to upload to Nekobin: {e.response.status_code}")
	except Exception:
		message.edit_text("Error: failed to upload to Nekobin: unknown error")
	else:
		message.edit_text(f"Done, uploaded to Nekobin: {url}", disable_web_page_preview=True)
