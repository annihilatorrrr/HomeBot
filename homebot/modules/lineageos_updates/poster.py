from homebot.core.database import HomeBotDatabase
from homebot.lib.liblineage.ota import FullUpdateInfo
from homebot.lib.liblineage.wiki import get_device_data
from homebot.core.config import get_config
from telegram.bot import Bot
from telegram.parsemode import ParseMode
from telegram.utils.helpers import escape_markdown

LINEAGEOS_TO_ANDROID_VERSION = {
	"16.0": "p",
	"17.1": "q",
	"18.1": "r",
	"19.0": "s",
}

class Poster:
	def __init__(self, bot: Bot):
		self.bot = bot

		self.chat_id = get_config("lineageos_updates.chat_id", "")
		if self.chat_id == "":
			raise AssertionError("No chat ID defined")

		self.photo_url_base = get_config("lineageos_updates.photo_url_base", "")
		if self.chat_id == "":
			raise AssertionError("No photo URL base defined")

		self.donation_link = get_config("lineageos_updates.donation_link", "")

	def post(self, codename: str, update: FullUpdateInfo):
		device_data = get_device_data(codename)
		caption = (
			f"{escape_markdown(f'#{codename}', 2)} \#lineageos {escape_markdown(f'#{LINEAGEOS_TO_ANDROID_VERSION[update.version]}', 2)}\n"
			f"LineageOS {escape_markdown(update.version, 2)} for {escape_markdown(device_data.name, 2)} {escape_markdown(f'({codename})', 2)}\n"
			f"\n"
			f"⚡️Build date: {escape_markdown(update.datetime.strftime('%Y/%m/%d'), 2)}\n"
			f"⚡️Download: [ROM & Recovery]({escape_markdown(f'https://download.lineageos.org/{codename}', 2)})\n"
			f"\n"
			f"Sources: {escape_markdown('https://github.com/LineageOS', 2)}\n"
			f"\n"
		)
		if self.donation_link != "":
			caption += f"Wanna buy me a coffee? {escape_markdown(self.donation_link, 2)}"

		message = self.bot.send_photo(chat_id=self.chat_id,
		                              photo=f"{self.photo_url_base}/{codename}.png",
		                              caption=caption,
		                              parse_mode=ParseMode.MARKDOWN_V2)

		if HomeBotDatabase.has(f"lineageos_updates.{codename}.last_message_id"):
			message_id = HomeBotDatabase.get(f"lineageos_updates.{codename}.last_message_id")
			try:
				self.bot.unpin_chat_message(chat_id=self.chat_id, message_id=message_id)
			except Exception:
				pass

		try:
			message.pin(disable_notification=True)
		except Exception:
			pass

		HomeBotDatabase.set(f"lineageos_updates.{codename}.last_message_id", message.message_id)
