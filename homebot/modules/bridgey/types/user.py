from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
	from homebot.modules.bridgey.platform import PlatformBase

class User:
	"""
	A class representing a user.

	Attributes:
	- platform (PlatformBase): The platform this user is from
	- name: The user's name
	- username: The user's username
	- avatar_url: The user's avatar URL
	"""
	def __init__(self,
	             platform: PlatformBase,
				 name: str,
				 username: str = "",
				 avatar_url: str = "",
				):
		self.platform = platform
		self.name = name
		self.username = username
		self.avatar_url = avatar_url

		if not self.avatar_url and self.platform.ICON_URL:
			self.avatar_url = self.platform.ICON_URL

	def __str__(self) -> str:
		"""
		Returns the formatted user name.

		It doesn't contain the platform name inside it because
		platforms can handle it as they wish.
		"""
		signature = f"{self.name}"

		if self.username:
			signature += f" (@{self.username})"

		return signature
