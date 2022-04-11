from homebot.core.config import get_config
from homebot.core.database import HomeBotDatabase
from homebot.lib.liblogging import LOGW
from homebot.modules.bridgey.platform import PlatformBase
from threading import Lock

# Platforms
from homebot.modules.bridgey.platforms.discord import DiscordPlatform
from homebot.modules.bridgey.platforms.matrix import MatrixPlatform
from homebot.modules.bridgey.platforms.telegram import TelegramPlatform

PLATFORMS: dict[str, PlatformBase] = {
	DiscordPlatform.NAME: DiscordPlatform,
	MatrixPlatform.NAME: MatrixPlatform,
	TelegramPlatform.NAME: TelegramPlatform,
}

class Pool:
	"""A class representing a pool (a group of connected chats)."""
	def __init__(self, name: str) -> None:
		"""Initialize the pool."""
		self.name = name

		self.database_key_prefix = f"bridgey.pools.{self.name}"
		self.last_message_id_key = f"{self.database_key_prefix}.last_message_id"
		self.messages_key = f"{self.database_key_prefix}.messages"
		self.platforms_key = f"{self.database_key_prefix}.platforms"

		self.last_message_id = (HomeBotDatabase.get(self.last_message_id_key)
		                        if HomeBotDatabase.has(self.last_message_id_key)
		                        else 0)
		self.last_message_id_lock = Lock()

		self.platforms: dict[str, PlatformBase] = {}

		for platform_name, platform_data in get_config(f"bridgey.pools.{self.name}", {}).items():
			if not "platform" in platform_data:
				LOGW(f"Pool {self.name} has an invalid platform, skipping")
				continue

			platform_type = platform_data["platform"]

			if not platform_type in PLATFORMS:
				LOGW(f"Pool {self.name} has an invalid platform type, skipping")
				continue

			platform_class = PLATFORMS[platform_type]

			self.platforms[platform_name] = (platform_class(self, platform_name, platform_data))

	def get_new_message_id(self) -> int:
		"""Reserve a new generic message ID."""
		with self.last_message_id_lock:
			self.last_message_id += 1
			HomeBotDatabase.set(self.last_message_id_key, self.last_message_id)
			return self.last_message_id

	def on_message(self, message, original_message_id: int) -> None:
		message_id = self.get_new_message_id()

		message.platform.set_platform_message_id(message_id, original_message_id)

		for platform in self.platforms.values():
			# Skip platform where the message is from
			if platform is message.platform:
				continue

			platform.send_message(message, message_id)
