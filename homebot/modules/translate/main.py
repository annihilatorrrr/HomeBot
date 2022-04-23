from deepl import Translator
from homebot.core.config import get_config
from sebaubuntu_libs.liblogging import LOGE
from telegram.ext import CallbackContext
from telegram.parsemode import ParseMode
from telegram.update import Update
from telegram.utils.helpers import escape_markdown

DEEPL_API_KEY = get_config("translate.deepl_api_key", "")

DEFAULT_LANG = "en-us"
TRANSLATOR = Translator(DEEPL_API_KEY)

def translate(update: Update, context: CallbackContext):
	reply_to_message = update.effective_message.reply_to_message
	if not reply_to_message:
		update.effective_message.reply_text("Please reply to a message to translate it")
		return

	text = reply_to_message.text if reply_to_message.text else reply_to_message.caption
	if not text:
		update.effective_message.reply_text("No text to translate")
		return

	if not DEEPL_API_KEY:
		update.effective_message.reply_text("API key not set, if you're a user it's not your fault")
		LOGE("DeepL API key not set")
		return

	usage = TRANSLATOR.get_usage()
	if usage.character.limit_exceeded:
		update.effective_message.reply_text("API character limit exceeded")
		return

	if context.args and len(context.args) > 0:
		to_lang = context.args[0]
	else:
		to_lang = DEFAULT_LANG

	try:
		text_result = TRANSLATOR.translate_text(text, target_lang=to_lang)
	except Exception as e:
		update.effective_message.reply_text(f"Error while translating the message, `{escape_markdown(to_lang, 2)}` is probably wrong: {escape_markdown(str(e), 2)}",
		                                    parse_mode=ParseMode.MARKDOWN_V2)
		return

	reply_text = (
		f"From `{escape_markdown(text_result.detected_source_lang, 2)}` to `{escape_markdown(to_lang, 2)}`:\n"
		"\n"
		f"{escape_markdown(text_result.text, 2)}"
	)

	update.effective_message.reply_text(reply_text, parse_mode=ParseMode.MARKDOWN_V2)
