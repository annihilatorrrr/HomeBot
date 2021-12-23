import json
from pathlib import Path
from threading import Lock

class _DatabaseFile:
	"""HomeBot database file class."""
	__file_name = "data.json"

	__file_path = Path(__file_name)
	__file_lock = Lock()

	@classmethod
	def load(cls):
		with cls.__file_lock:
			if cls.__file_path.is_file():
				return json.loads(cls.__file_path.read_bytes())

			return {}

	@classmethod
	def dump(cls, d: dict):
		with cls.__file_lock:
			cls.__file_path.write_text(json.dumps(d, indent=4, sort_keys=True))

class HomeBotDatabase:
	"""HomeBot database class.

	This class is used to save persistent data.
	"""

	ALLOWED_DATA_TYPES = [
		bool,
		dict,
		float,
		int,
		list,
		# TODO: With 3.10 move to types.NoneType
		type(None),
		str,
	]
	"""List of allowed values data types."""

	__dict = _DatabaseFile.load()
	__dict_lock = Lock()

	@classmethod
	def _has(cls, k: str):
		"""Unprotected cls.has implementation."""
		if type(k) is not str:
			raise TypeError("Key isn't a string")

		if not '.' in k:
			value = k in cls.__dict
		else:
			value = cls.__dict
			for subkey in k.split('.'):
				if subkey not in value:
					value = False
					break

				value = value[subkey]

		return value

	@classmethod
	def has(cls, k: str):
		"""Check if a key is inside the database."""
		with cls.__dict_lock:
			return cls._has(k)

	@classmethod
	def _get(cls, k: str):
		"""Unprotected cls.get implementation."""
		if type(k) is not str:
			raise TypeError("Key isn't a string")

		if not '.' in k:
			value = cls.__dict[k]
		else:
			value = cls.__dict
			for subkey in k.split('.'):
				value = value[subkey]

		return value

	@classmethod
	def get(cls, k: str):
		"""Get a value from the database."""
		with cls.__dict_lock:
			return cls._get(k)

	@classmethod
	def _set(cls, k: str, v):
		"""Unprotected cls.set implementation."""
		if type(k) is not str:
			raise TypeError("Key isn't a string")

		if type(v) not in cls.ALLOWED_DATA_TYPES:
			raise TypeError("Value data type not allowed")

		if not '.' in k:
			if cls._has(k) and isinstance(cls._get(k), dict):
					cls._get(k).update(v)
			else:
				cls.__dict[k] = v
		else:
			d = v
			for subkey in k.split('.')[::-1]:
				d = {subkey: d}
				subkey_full = k.removesuffix(f".{subkey}")
				if cls._has(subkey_full) and isinstance(cls._get(subkey_full), dict):
					cls._get(subkey_full).update(d)
					d = cls._get(subkey_full)

			cls.__dict.update(d)

		cls._dump()

	@classmethod
	def set(cls, k: str, v):
		"""Save a value to the database."""
		with cls.__dict_lock:
			return cls._set(k, v)

	@classmethod
	def _dump(cls):
		"""Dump the database to file."""
		_DatabaseFile.dump(cls.__dict)
