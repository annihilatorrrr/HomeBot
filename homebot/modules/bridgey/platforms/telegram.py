from homebot.modules.bridgey.platform import PlatformBase
from homebot.modules.bridgey.types.file import File
from homebot.modules.bridgey.types.message import Message, MessageType
from homebot.modules.bridgey.types.user import User
import requests
from sebaubuntu_libs.libexception import format_exception
from sebaubuntu_libs.liblogging import LOGE, LOGI
from telegram import File as TelegramFile
from telegram.bot import Bot
from telegram.error import BadRequest
from telegram.message import Message as TelegramMessage
from telegram.user import User as TelegramUser

posters: list[Bot] = []

class TelegramPlatform(PlatformBase):
	NAME = "Telegram"
	ICON_URL = "https://telegram.org/img/t_logo.png"
	FILE_TYPE = TelegramFile
	MESSAGE_TYPE = TelegramMessage
	USER_TYPE = TelegramUser

	def __init__(self, pool, instance_name: str, data: dict):
		super().__init__(pool, instance_name, data)

		self.chat_id: int = data["chat_id"]

	@property
	def running(self) -> bool:
		return True

	def file_to_generic(self, file: FILE_TYPE) -> Message:
		return File(platform=self,
		            url=file.file_path)

	def user_to_generic(self, user: USER_TYPE) -> User:
		try:
			user_propics = user.get_profile_photos().photos
		except BadRequest:
			user_propics = []

		if user_propics:
			avatar_url = user_propics[0][0].get_file().file_path
		else:
			avatar_url = ""

		return User(platform=self,
		            name=user.full_name,
		            username=user.username,
					url=f"https://t.me/{user.username}" if user.username else "",
		            avatar_url=avatar_url)

	def message_to_generic(self, message: MESSAGE_TYPE) -> Message:
		text = ""
		file = None
		sticker_emoji = ""
		reply_to = None

		if message.text:
			message_type = MessageType.TEXT
			text = message.text
		elif message.photo:
			message_type = MessageType.IMAGE
			text = message.caption
			file = message.photo[-1].get_file()
		elif message.video or message.animation:
			message_type = (MessageType.ANIMATION if message.animation else MessageType.VIDEO)
			text = message.caption
			file = (message.animation if message.animation else message.video).get_file()
		elif message.audio or message.voice:
			message_type = MessageType.AUDIO
			text = message.caption
			file = (message.voice if message.voice else message.audio).get_file()
		elif message.sticker:
			message_type = MessageType.STICKER
			file = message.sticker.thumb.get_file()
			sticker_emoji = message.sticker.emoji
		elif message.document:
			message_type = MessageType.DOCUMENT
			text = message.caption
			file = message.document.get_file()
		else:
			message_type = MessageType.UNKNOWN

		if message.reply_to_message:
			reply_to = self.get_generic_message_id(message.reply_to_message.message_id)

		return Message(platform=self,
		               message_type=message_type,
		               user=self.user_to_generic(message.from_user),
		               timestamp=message.date,
		               text=text if text else "",
		               file=self.file_to_generic(file) if file else None,
					   sticker_emoji=sticker_emoji,
		               reply_to=reply_to)

	def send_message(self, message: Message, message_id: int) -> None:
		text = f"[{message.platform.NAME}] {message.user}:"
		if message.text:
			text += f"\n{message.text}"

		if message.file:
			try:
				r = requests.get(message.file.url)
			except Exception as e:
				LOGE(f"Failed to download file: {e}")
				return

		reply_to_message_id = None
		if message.reply_to:
			reply_to_message_id = self.get_platform_message_id(message.reply_to)

		for bot in posters:
			try:
				if message.message_type == MessageType.TEXT:
					telegram_message = bot.send_message(chat_id=self.chat_id, text=text, reply_to_message_id=reply_to_message_id)
				elif message.message_type == MessageType.IMAGE:
					telegram_message = bot.send_photo(chat_id=self.chat_id, photo=r.content, filename=message.file.name, caption=text, reply_to_message_id=reply_to_message_id)
				elif message.message_type == MessageType.VIDEO:
					telegram_message = bot.send_video(chat_id=self.chat_id, video=r.content, filename=message.file.name, caption=text, reply_to_message_id=reply_to_message_id)
				elif message.message_type == MessageType.AUDIO:
					telegram_message = bot.send_audio(chat_id=self.chat_id, audio=r.content, filename=message.file.name, caption=text, reply_to_message_id=reply_to_message_id)
				elif message.message_type == MessageType.DOCUMENT:
					telegram_message = bot.send_document(chat_id=self.chat_id, document=r.content, filename=message.file.name, caption=text, reply_to_message_id=reply_to_message_id)
				elif message.message_type == MessageType.STICKER:
					telegram_message = bot.send_sticker(chat_id=self.chat_id, sticker=r.content, reply_to_message_id=reply_to_message_id)
				elif message.message_type == MessageType.ANIMATION:
					telegram_message = bot.send_animation(chat_id=self.chat_id, animation=r.content, filename=message.file.name, caption=text, reply_to_message_id=reply_to_message_id)
				else:
					LOGI(f"Unknown message type: {message.message_type}")
			except Exception as e:
				LOGI(f"Failed to send message: {format_exception(e)}, retrying with different bot")
				continue

			self.set_platform_message_id(message_id, telegram_message.message_id)

			break
