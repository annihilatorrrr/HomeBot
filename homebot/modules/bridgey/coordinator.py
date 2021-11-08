from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
	from homebot.modules.bridgey.platform import PlatformBase
	from homebot.modules.bridgey.types.message import Message

# Platforms
from homebot.modules.bridgey.platforms.discord import DiscordPlatform
from homebot.modules.bridgey.platforms.telegram import TelegramPlatform

class _Coordinator:
	"""This class is responsible for coordinating the message passing between platforms"""
	def __init__(self):
		self.platforms: dict[PlatformBase, PlatformBase] = {
			DiscordPlatform: DiscordPlatform(self),
			TelegramPlatform: TelegramPlatform(self),
		}

	def handle_message(self, message: Message):
		for platform, platform_instance in self.platforms.items():
			if platform == message.platform:
				continue

			platform_instance.send_message(message)

class Coordinator(_Coordinator):
	DEFAULT = _Coordinator()
