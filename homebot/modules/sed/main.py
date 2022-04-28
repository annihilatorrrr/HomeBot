import re
from telegram.ext import CallbackContext
from telegram.update import Update

def sed(update: Update, context: CallbackContext):
	if not update.message.reply_to_message:
		return

	string = update.message.reply_to_message.text

	if not string:
		return

	message_text = update.message.text
	if not message_text:
		return

	if not message_text.startswith("s/"):
		return

	sed_command = message_text.split("/")
	if len(sed_command) < 3 or len(sed_command) > 4:
		return

	pattern = sed_command[1]
	repl = sed_command[2]
	if len(sed_command) == 4:
		flags = sed_command[3]
	else:
		flags = ""

	# flags parsing
	all_matches = 'g' in flags
	ignorecase = 'i' in flags or 'I' in flags
	multiline = 'm' in flags or 'M' in flags

	flags = 0
	flags |= (re.M if multiline else 0)
	flags |= (re.I if ignorecase else 0)

	force_reply = False
	try:
		result = re.sub(pattern, repl, string, (0 if all_matches else 1), flags)
	except Exception as e:
		result = (
			f"fuck me\n"
			f"{e}"
		)
		force_reply = True

	if not force_reply and result == string:
		return

	if not result:
		result = "Result is an empty string you fuck"

	update.message.reply_text(result)
