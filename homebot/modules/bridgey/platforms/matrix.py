from __future__ import annotations
from datetime import datetime
from homebot.core.config import get_config
from homebot.core.database import HomeBotDatabase
from homebot.lib.libexception import format_exception
from homebot.lib.liblogging import LOGE
from homebot.modules.bridgey.platform import PlatformBase
from homebot.modules.bridgey.types.file import File
from homebot.modules.bridgey.types.message import Message, MessageType
from homebot.modules.bridgey.types.user import User
import magic
from matrix_client.client import MatrixClient, MatrixRequestError
from matrix_client.room import Room
import requests

ENABLE = get_config("bridgey.matrix.enable", False)
USERNAME = get_config("bridgey.matrix.username", "")
PASSWORD = get_config("bridgey.matrix.password", "")
HOMESERVER_URL = get_config("bridgey.matrix.homeserver_url", "")
ROOM_ALIAS = get_config("bridgey.matrix.room_alias", "")

DATA_IS_VALID = bool(ENABLE and USERNAME and PASSWORD and HOMESERVER_URL and ROOM_ALIAS)

class MatrixPlatform(PlatformBase):
	NAME = "Matrix"
	ICON_URL = "https://matrix.org/blog/wp-content/uploads/2015/01/logo1.png"
	FILE_TYPE = str
	MESSAGE_TYPE = dict
	USER_TYPE = str

	def __init__(self, coordinator):
		super().__init__(coordinator)

		self.client = None
		self.room = None
		self.thread = None

		if not ENABLE:
			return

		if not DATA_IS_VALID:
			LOGE("Missing or invalid Matrix configuration")
			return

		if HomeBotDatabase.has("bridgey.matrix.logged_in") and HomeBotDatabase.get("bridgey.matrix.logged_in"):
			self.client = MatrixClient(HOMESERVER_URL, token=HomeBotDatabase.get("bridgey.matrix.token"),
			                           user_id=HomeBotDatabase.get("bridgey.matrix.user_id"))
			self.client.device_id = HomeBotDatabase.get("bridgey.matrix.device_id")
		else:
			self.client = MatrixClient(HOMESERVER_URL)
			try:
				token = self.client.login(USERNAME, PASSWORD, sync=False)
			except MatrixRequestError as e:
				LOGE(f"Failed to login: {format_exception(e)}")
				return

			HomeBotDatabase.set("bridgey.matrix.token", token)
			HomeBotDatabase.set("bridgey.matrix.device_id", self.client.device_id)
			HomeBotDatabase.set("bridgey.matrix.user_id", self.client.user_id)
			HomeBotDatabase.set("bridgey.matrix.logged_in", True)

		try:
			self.room: Room = self.client.join_room(ROOM_ALIAS)
		except MatrixRequestError as e:
			LOGE(f"Failed to join room: {format_exception(e)}")
			return

		self.room.add_listener(self.handle_msg, "m.room.message")
		self.client.start_listener_thread()
		self.thread = self.client.sync_thread

	@property
	def running(self):
		return DATA_IS_VALID and self.thread and self.thread.is_alive()

	def file_to_generic(self, file: FILE_TYPE) -> Message:
		return File(platform=MatrixPlatform,
		            url=self.client.api.get_download_url(file))

	def user_to_generic(self, user: USER_TYPE) -> User:
		avatar_url = self.client.api.get_avatar_url(user)
		return User(platform=MatrixPlatform,
		            name=user,
					url=f"https://matrix.to/#/{user}",
		            avatar_url=self.client.api.get_download_url(avatar_url))

	def message_to_generic(self, message: MESSAGE_TYPE) -> Message:
		content = message["content"]
		message_type = MessageType.UNKNOWN
		text = ""
		file = None
		reply_to = None

		if content["msgtype"] == "m.text":
			message_type = MessageType.TEXT
		elif content["msgtype"] == "m.image":
			message_type = MessageType.IMAGE
		elif content["msgtype"] == "m.video":
			message_type = MessageType.VIDEO
		elif content["msgtype"] == "m.audio":
			message_type = MessageType.AUDIO
		elif content["msgtype"] == "m.file":
			message_type = MessageType.DOCUMENT

		if "body" in content:
			text = content["body"]

		user = self.user_to_generic(message["sender"])

		if "url" in content:
			file = self.file_to_generic(content["url"])

		if ("m.relates_to" in content and "m.in_reply_to" in content["m.relates_to"]
		    and "event_id" in content["m.relates_to"]["m.in_reply_to"]):
			in_reply_to = content['m.relates_to']['m.in_reply_to']['event_id']
			reply_to = reply_to = self.get_generic_message_id(in_reply_to)

		return Message(platform=MatrixPlatform,
		               message_type=message_type,
		               user=user,
		               timestamp=datetime.now(),
		               text=text,
		               file=file,
					   reply_to=reply_to)

	def handle_msg(self, room: Room, event: dict):
		# Make sure we didn't send this message
		if event['sender'] == self.client.user_id:
			return

		message_id = self.on_message(self.message_to_generic(event))
		HomeBotDatabase.set(f"bridgey.messages.{message_id}.{self.NAME}", event["event_id"])

	def send_message(self, message: Message, message_id: int):
		if not self.running:
			return

		text = f"[{message.platform.NAME}] {message.user}:"
		if message.text:
			text += f"\n{message.text}"

		if message.message_type.is_file():
			try:
				r = requests.get(message.file.url)
			except Exception as e:
				LOGE(f"Failed to download file: {e}")
				return
			try:
				mime_type = magic.from_buffer(r.content, mime=True)
				url = self.client.upload(content=r.content, content_type=mime_type, filename=message.file.name)
			except Exception as e:
				LOGE(f"Failed to upload file: {format_exception(e)}")
				return
		else:
			url = None

		if message.message_type is MessageType.TEXT:
			matrix_message = self.room.send_text(text)
		elif message.message_type is MessageType.IMAGE or message.message_type is MessageType.STICKER:
			matrix_message = self.room.send_image(url, message.file.name, body=text)
		elif message.message_type is MessageType.VIDEO or message.message_type is MessageType.ANIMATION:
			matrix_message = self.room.send_video(url, message.file.name,body=text)
		elif message.message_type is MessageType.AUDIO:
			matrix_message = self.room.send_audio(url, message.file.name, body=text)
		elif message.message_type is MessageType.DOCUMENT:
			matrix_message = self.room.send_file(url, message.file.name, body=text)
		else:
			LOGE(f"Unknown message type: {message.message_type}")
			return

		HomeBotDatabase.set(f"bridgey.messages.{message_id}.{self.NAME}", matrix_message["event_id"])
