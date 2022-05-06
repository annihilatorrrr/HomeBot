from __future__ import annotations
import asyncio
from discord import Client, Embed, File as DiscordFile, TextChannel
from discord import Attachment, Message as DiscordMessage, User as DiscordUser
from homebot.modules.bridgey.platform import PlatformBase
from homebot.modules.bridgey.types.file import File
from homebot.modules.bridgey.types.message import Message, MessageType
from homebot.modules.bridgey.types.user import User
from io import BytesIO
import requests
from sebaubuntu_libs.liblogging import LOGE
from threading import Thread

class BridgeyDiscordClient(Client):
	"""Discord client that pass the message to DiscordPlatform."""
	def __init__(self, platform: DiscordPlatform, *, loop=None, **options):
		"""Initialize the client."""
		super().__init__(loop=loop, **options)

		self.platform = platform

	async def on_ready(self):
		channel = self.get_channel(self.platform.channel_id)

		if not channel:
			LOGE(f"Failed to get channel {self.platform.channel_id}")
			return

		if not isinstance(channel, TextChannel):
			LOGE(f"Channel {self.platform.channel_id} is not a text channel")
			return

		self.platform.channel = channel

	async def on_message(self, message: DiscordMessage):
		if message.author == self.user:
			return
		if message.channel.id != self.platform.channel_id:
			return

		self.platform.on_message(self.platform.message_to_generic(message), message.id)

	def run_coroutine(self, coroutine):
		"""Run a coroutine in the client's loop."""
		return asyncio.run_coroutine_threadsafe(coroutine, self.loop).result()

class DiscordPlatform(PlatformBase):
	"""Discord platform."""
	NAME = "Discord"
	ICON_URL = "https://discord.com/assets/f9bb9c4af2b9c32a2c5ee0014661546d.png"
	FILE_TYPE = Attachment
	MESSAGE_TYPE = DiscordMessage
	USER_TYPE = DiscordUser

	def __init__(self, pool, instance_name: str, data: dict):
		"""Initialize the platform."""
		super().__init__(pool, instance_name, data)

		self.channel_id: int = data["channel_id"]
		self.token: str = data["token"]

		self.client = None
		self.channel: TextChannel = None
		self.thread = None

		self.client = BridgeyDiscordClient(self)

		self.thread = Thread(target=self.__daemon, daemon=True)
		self.thread.start()

	def __daemon(self):
		self.client.run(self.token)

	@property
	def running(self) -> bool:
		return bool(self.thread) and self.thread.is_alive() and self.channel is not None

	def file_to_generic(self, file: FILE_TYPE) -> Message:
		return File(platform=self,
		            url=file.url,
		            name=file.filename)

	def user_to_generic(self, user: USER_TYPE) -> User:
		return User(platform=self,
		            name=f"{user.name}#{user.discriminator}",
					url=f"https://discordapp.com/users/{user.id}",
					avatar_url=user.avatar)

	def message_to_generic(self, message: MESSAGE_TYPE) -> Message:
		message_type = MessageType.TEXT
		text = message.content
		file = None
		reply_to = None

		if message.attachments:
			message_type = MessageType.DOCUMENT
			file = message.attachments[0]
			if file.content_type:
				file_type = str(file.content_type)
				if file_type.startswith("audio/"):
					message_type = MessageType.AUDIO
				elif file_type.startswith("image/"):
					message_type = MessageType.IMAGE
				elif file_type.startswith("video/"):
					message_type = MessageType.VIDEO

			if len(message.attachments) > 1:
				text += "\n[Additional attached files]"
				for attachment in message.attachments[1:]:
					text += f"\n - {attachment.url}"

		if message.reference:
			reply_to = self.get_generic_message_id(message.reference.message_id)

		return Message(platform=self,
		               message_type=message_type,
		               user=self.user_to_generic(message.author),
					   timestamp=message.created_at,
		               text=text,
					   file=self.file_to_generic(file) if file else None,
					   reply_to=reply_to)

	def send_message(self, message: Message, message_id: int) -> None:
		if not self.running:
			return

		title = ""
		description = message.text
		file = None

		if message.message_type is MessageType.STICKER:
			title = "Sticker"
			description = message.sticker_emoji

		embed = Embed(title=title, description=description, timestamp=message.timestamp)
		embed.set_author(name=str(message.user), url=message.user.url,
		                 icon_url=message.user.avatar_url)
		embed.set_footer(text=message.platform.NAME, icon_url=message.platform.ICON_URL)

		if message.file:
			# This thing leaks bot token...
			# This way Discord keeps the original URL that contains the token
			#if message.message_type is MessageType.IMAGE:
			#	embed.set_image(url=message.file.url)
			#elif message.message_type is MessageType.STICKER:
			#	embed.set_thumbnail(url=message.file.url)
			#else:
				try:
					r = requests.get(message.file.url)
				except Exception as e:
					LOGE(f"Failed to download file: {e}")
					return

				file = DiscordFile(BytesIO(r.content), filename=message.file.name)

		reference = None
		if message.reply_to:
			reply_to_message_id = self.get_platform_message_id(message.reply_to)
			if reply_to_message_id is not None:
				reference = self.channel.get_partial_message(reply_to_message_id)

		try:
			discord_message = self.client.run_coroutine(self.channel.send(embed=embed,
			                                                              file=file,
			                                                              reference=reference))
		except Exception as e:
			LOGE(f"Failed to send message to Discord: {e}")
			return

		self.set_platform_message_id(message_id, discord_message.id)
