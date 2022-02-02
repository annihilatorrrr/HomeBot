from __future__ import annotations
from homebot.core.database import HomeBotDatabase
from threading import Lock
from typing import TYPE_CHECKING
if TYPE_CHECKING:
	from homebot.modules.bridgey.platform import PlatformBase
	from homebot.modules.bridgey.types.message import Message

# Platforms
from homebot.modules.bridgey.platforms.discord import DiscordPlatform
from homebot.modules.bridgey.platforms.matrix import MatrixPlatform
from homebot.modules.bridgey.platforms.telegram import TelegramPlatform

class _Coordinator:
	"""This class is responsible for coordinating the message passing between platforms"""
	def __init__(self):
		self.last_message_id = 0
		if HomeBotDatabase.has("bridgey.last_message_id"):
			self.last_message_id = HomeBotDatabase.get("bridgey.last_message_id")
		self.last_message_id_lock = Lock()
		self.platforms: dict[PlatformBase, PlatformBase] = {
			DiscordPlatform: DiscordPlatform(self),
			MatrixPlatform: MatrixPlatform(self),
			TelegramPlatform: TelegramPlatform(self),
		}

	def get_new_message_id(self) -> int:
		"""Reserve a new generic message ID."""
		with self.last_message_id_lock:
			self.last_message_id += 1
			HomeBotDatabase.set("bridgey.last_message_id", self.last_message_id)
			return self.last_message_id

	def handle_message(self, message: Message):
		message_id = self.get_new_message_id()

		for platform, platform_instance in self.platforms.items():
			if platform == message.platform:
				continue

			platform_instance.send_message(message, message_id)

		return message_id

class Coordinator(_Coordinator):
	DEFAULT = _Coordinator()
