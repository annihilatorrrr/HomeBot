from homebot import __version__
from homebot.core.bot import HomeBot
from homebot.core.config import get_config
from homebot.core.logging import setup_logging
from homebot.lib.liblogging import LOGI

def main():
	setup_logging()
	updater = HomeBot(get_config("bot.api_token"))
	LOGI(f"HomeBot started, version {__version__}")
	LOGI(f"Bot username: @{updater.bot.get_me().username}")
	updater.start_polling()
	updater.idle()

	LOGI("Stopping HomeBot...")
	exit()
