from datetime import datetime
from homebot.modules.lineageos_updates.device_data import DeviceData
from homebot.core.config import get_config
from telegram.bot import Bot

LINEAGEOS_TO_ANDROID_VERSION = {
	"16.0": "p",
	"17.1": "q",
	"18.1": "r",
}

posters = {}

class Poster:
	def __init__(self, bot: Bot):
		self.bot = bot

		self.chat_id = get_config("lineageos_updater.chat_id", "")
		if self.chat_id == "":
			raise AssertionError("No chat ID defined")

		self.photo_url_base = get_config("lineageos_updater.photo_url_base", "")
		if self.chat_id == "":
			raise AssertionError("No photo URL base defined")

		self.donation_link = get_config("lineageos_updater.donation_link", "")

	def post(self, device_data: DeviceData, build_date: int, version: str):
		date = datetime.fromtimestamp(build_date)
		caption = (
			f"#{device_data.codename} #lineageos #{LINEAGEOS_TO_ANDROID_VERSION[version]}\n"
			f"LineageOS {version} Official for {device_data.name} ({device_data.codename})\n"
			f"\n"
			f"⚡️Build date: {str(date.year)}/{str(date.month)}/{str(date.day)}\n"
			f"⚡️Download: [ROM & Recovery](https://download.lineageos.org/{device_data.codename})\n"
			f"\n"
			f"Sources: https://github.com/LineageOS\n"
			f"\n"
		)
		if self.donation_link != "":
			caption += f"Wanna buy me a coffee? {self.donation_link}"

		self.bot.send_photo(chat_id=self.chat_id,
		                    photo=f"{self.photo_url_base}/{device_data.codename}.png",
		                    caption=caption,
							parse_mode="Markdown")
