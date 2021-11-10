from __future__ import annotations
import asyncio
from discord import Client, Embed, File as DiscordFile, RequestsWebhookAdapter, Webhook
from discord import Attachment, Message as DiscordMessage, User as DiscordUser
from homebot.core.config import get_config
from homebot.core.logging import LOGE
from homebot.modules.bridgey.platform import PlatformBase
from homebot.modules.bridgey.types.file import File
from homebot.modules.bridgey.types.message import Message, MessageType
from homebot.modules.bridgey.types.user import User
from io import BytesIO
import requests
from threading import Thread

ENABLE = get_config("bridgey.discord.enable", False)
CHANNEL_ID = get_config("bridgey.discord.channel_id", None)
TOKEN = get_config("bridgey.discord.token", "")
WEBHOOK_URL = get_config("bridgey.discord.webhook_url", "")

class BridgeyDiscordClient(Client):
	"""Discord client that pass the message to DiscordPlatform."""
	def __init__(self, *, loop=None, **options):
		"""Initialize the client."""
		super().__init__(loop=loop, **options)

		self.platform = None

	def set_platform(self, platform: DiscordPlatform):
		self.platform = platform

	async def on_message(self, message: DiscordMessage):
		if message.author == self.user:
			return
		if message.channel.id != CHANNEL_ID:
			return
		if not self.platform:
			return
		if message.webhook_id and (self.platform.webhook.id == message.webhook_id):
			return

		if self.platform is not None:
			self.platform.on_message(message)

client = BridgeyDiscordClient()

def start_daemon():
	loop = asyncio.get_event_loop()
	loop.create_task(client.start(TOKEN))
	thread = Thread(target=loop.run_forever, daemon=True)
	thread.start()
	return thread

class DiscordPlatform(PlatformBase):
	"""Discord platform."""
	NAME = "Discord"
	ICON_URL = "https://discord.com/assets/f9bb9c4af2b9c32a2c5ee0014661546d.png"
	FILE_TYPE = Attachment
	MESSAGE_TYPE = DiscordMessage
	USER_TYPE = DiscordUser

	def __init__(self, coordinator):
		"""Initialize the platform."""
		super().__init__(coordinator)

		self.webhook = None
		self.thread = None

		if not (ENABLE and CHANNEL_ID and TOKEN and WEBHOOK_URL):
			return

		try:
			self.webhook = Webhook.from_url(WEBHOOK_URL, adapter=RequestsWebhookAdapter())
		except Exception as e:
			LOGE(f"Failed to create webhook: {e}")
			return

		client.set_platform(self)

		self.thread = start_daemon()

	@property
	def running(self) -> bool:
		return self.thread.is_alive() and self.webhook

	def file_to_generic(self, file: FILE_TYPE) -> Message:
		return File(platform=DiscordPlatform,
		            url=file.url,
		            name=file.filename)

	def user_to_generic(self, user: USER_TYPE) -> User:
		return User(platform=DiscordPlatform,
		            name=f"{user.name}#{user.discriminator}",
					avatar_url=user.avatar)

	def message_to_generic(self, message: MESSAGE_TYPE) -> Message:
		message_type = MessageType.TEXT
		text = message.content
		file = None

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

		return Message(platform=DiscordPlatform,
		               message_type=message_type,
		               user=self.user_to_generic(message.author),
					   timestamp=message.created_at,
		               text=text,
					   file=self.file_to_generic(file) if file else None)

	def send_message(self, message: Message) -> None:
		if not self.webhook:
			LOGE("Webhook is None")
			return

		title = ""
		description = message.text
		file = None

		if message.message_type is MessageType.STICKER:
			title = "Sticker"
			description = message.sticker_emoji

		embed = Embed(title=title, description=description, timestamp=message.timestamp)
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

		try:
			self.webhook.send(username=str(message.user), avatar_url=message.user.avatar_url,
			                  embed=embed, file=file)
		except Exception as e:
			LOGE(f"Failed to send message to Discord: {e}")
