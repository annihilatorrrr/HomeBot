from homebot.modules.bridgey.types.file import File
from homebot.modules.bridgey.types.message import Message
from homebot.modules.bridgey.types.user import User

class PlatformBase:
	"""Base class of a bridge platform"""
	# The name of the platform
	NAME: str = None
	# The icon of the platform, used to indicate platform and as a fallback for user avatar
	ICON_URL: str = None
	# The "native" file type of the platform
	FILE_TYPE: type = File
	# The "native" message type of the platform
	MESSAGE_TYPE: type = Message
	# The "native" user type of the platform
	USER_TYPE: type = User

	def __init__(self, coordinator):
		"""Initialize the platform."""
		self.coordinator = coordinator

	def __str__(self) -> str:
		"""Return the name of the platform."""
		return self.NAME

	@property
	def running(self) -> bool:
		"""The platform observer is running."""
		raise NotImplementedError

	def file_to_generic(self, file: FILE_TYPE) -> Message:
		"""Convert a platform-specific file object to a generic message."""
		raise NotImplementedError

	def user_to_generic(self, user: USER_TYPE) -> User:
		"""Convert a platform-specific user object to a generic user."""
		raise NotImplementedError

	def message_to_generic(self, message: MESSAGE_TYPE) -> Message:
		"""Convert a platform-specific message object to a generic message."""
		raise NotImplementedError

	def on_message(self, message: Message) -> None:
		"""A new message has been received and must be sent to other bridges."""
		self.coordinator.handle_message(message)

	def send_message(self, message: Message) -> None:
		"""Send a message to the platform."""
		raise NotImplementedError
