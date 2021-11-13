from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from homebot.modules.bridgey.platform import PlatformBase
	from homebot.modules.bridgey.types.file import File
	from homebot.modules.bridgey.types.user import User

from datetime import datetime

class _MessageType:
	(
		_TEXT,
		_IMAGE,
		_VIDEO,
		_AUDIO,
		_DOCUMENT,
		_STICKER,
		_ANIMATION,
		_UNKNOWN,
	) = range(8)

	_STRINGS = {
		_TEXT: "text",
		_IMAGE: "image",
		_VIDEO: "video",
		_AUDIO: "audio",
		_DOCUMENT: "document",
		_STICKER: "sticker",
		_ANIMATION: "animation",
		_UNKNOWN: "unknown",
	}

	_IS_FILE = [
		_IMAGE,
		_VIDEO,
		_AUDIO,
		_DOCUMENT,
		_STICKER,
		_ANIMATION,
	]

	def __init__(self, message_type):
		self.message_type = message_type

	def __int__(self) -> int:
		return self.message_type

	def __str__(self) -> str:
		return self._STRINGS[self.message_type]

	def is_file(self) -> bool:
		return self.message_type in self._IS_FILE

class MessageType(_MessageType):
	"""Class representing a message type.

	Available types:
	- TEXT: A simple text message, only text attribute must be filled.
	- IMAGE: An image message, file_url attribute must have a link to a valid image,
	         while text (interpreted as caption) might be filled.
	- VIDEO: A video message, file_url attribute must have a link to a valid video,
	         while text (interpreted as caption) might be filled.
	- AUDIO: An audio message, file_url attribute must have a link to a valid audio,
	         while text (interpreted as caption) might be filled.
	- DOCUMENT: A document message, file_url attribute must have a link to a valid document,
	            while text (interpreted as caption) might be filled.
	- STICKER: A sticker message, only file_url attribute must be filled with a link to a valid image.
	- ANIMATION: An animation message, file_url attribute must have a link to a valid video without audio,
	             while text (interpreted as caption) might be filled.
	- UNKNOWN: A message which isn't implemented, or is a special message type of the platform.
	           This type should always be avoided and instead convert unhandled types to a closer one
			   (for example, if a user send a contact, you can convert it
			   to a text message containing the contact's name and number).
	           Platforms will decide what to do with this message.
	"""
	TEXT = _MessageType(_MessageType._TEXT)
	IMAGE = _MessageType(_MessageType._IMAGE)
	VIDEO = _MessageType(_MessageType._VIDEO)
	AUDIO = _MessageType(_MessageType._AUDIO)
	DOCUMENT = _MessageType(_MessageType._DOCUMENT)
	STICKER = _MessageType(_MessageType._STICKER)
	ANIMATION = _MessageType(_MessageType._ANIMATION)
	UNKNOWN = _MessageType(_MessageType._UNKNOWN)

class Message:
	"""Class representing a message.

	Attributes:
	- platform: The platform where the message comes from
	- message_type: The type of the message (see MessageType class)
	- user: The user that sent the message (see User class)
	- timestamp: datetime object representing when the message has been sent
	- text: The text of the message, can be empty
	- file: The file of the message if message type requires it (see File class)
	- sticker_emoji: The emoji associated with a sticker, applicable only to MessageType.STICKER
	"""
	def __init__(self,
	             platform: PlatformBase,
	             message_type: MessageType,
	             user: User,
	             timestamp: datetime,
	             text: str = "",
	             file: File = None,
	             sticker_emoji: str = "",
	            ):
		"""Initialize the message."""
		self.platform = platform
		self.message_type = message_type
		self.user = user
		self.timestamp = timestamp
		self.text = text
		self.file = file
		self.sticker_emoji = sticker_emoji
