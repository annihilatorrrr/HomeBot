from homebot.lib.liblineage import GITHUB_ORG, LINEAGEOS_TO_ANDROID_VERSION
from homebot.lib.liblineage.ota import FullUpdateInfo
from homebot.lib.liblineage.wiki import get_device_data
from homebot.core.config import get_config
from telegram.bot import Bot
from telegram.parsemode import ParseMode
from telegram.utils.helpers import escape_markdown

class Poster:
	def __init__(self, bot: Bot):
		self.bot = bot

		self.chat_id = get_config("lineageos_updates.chat_id")

		if not get_config("lineageos_updates.enable", False):
			return

	def post(self, codename: str, update: FullUpdateInfo):
		chat = self.bot.get_chat(chat_id=self.chat_id)
		device_data = get_device_data(codename)
		text = (
			f"{escape_markdown(f'#{codename}', 2)} {escape_markdown(f'#{LINEAGEOS_TO_ANDROID_VERSION[update.version].version_short.lower()}', 2)}\n"
			f"*LineageOS {escape_markdown(update.version, 2)} for {escape_markdown(device_data.name, 2)} {escape_markdown(f'({codename})', 2)}*\n"
			f"\n"
			f"Build date: {escape_markdown(update.datetime.strftime('%Y/%m/%d'), 2)}\n"
			f"Download: [Here]({escape_markdown(f'https://download.lineageos.org/{codename}', 2)})\n"
			f"Device wiki page: [Here]({escape_markdown(f'https://wiki.lineageos.org/devices/{codename}', 2)})\n"
			f"Installation instructions: [Here]({escape_markdown(f'https://wiki.lineageos.org/devices/{codename}/install', 2)})\n"
			f"\n"
		)
		if chat.username:
			text += (
				f"@{chat.username}\n"
			)

		chat.send_message(text, parse_mode=ParseMode.MARKDOWN_V2)
