from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
	from homebot.modules.bridgey.platform import PlatformBase

from os.path import basename

class File:
	"""Class representing a file.

	Attributes:
	- platform: The platform this file is from.
	- url: The url of the file.
	- name: The name of the file. When not provided it will become the basename of the URL.
	"""
	def __init__(self,
	             platform: PlatformBase,
	             url: str,
	             name: str = "",
	            ) -> None:
		"""Initialize file class."""
		self.platform = platform
		self.url = url
		self.name = name

		if not self.name:
			self.name = basename(self.url)
