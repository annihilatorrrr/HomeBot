import pickle
from threading import Lock

DATABASE_FILE_NAME = "data.pkl"

class HomeBotDatabase:
	def __init__(self):
		"""Initialize the database."""
		self.fd = open(DATABASE_FILE_NAME, 'wb')

		self.data = pickle.load(self.fd)
		self.lock = Lock()

	def get(self, key, default=None):
		with self.lock:
			if not key in self.data:
				return default

			return self.data[key]

	def set(self, key, value):
		with self.lock:
			self.data[key] = value
			self._sync()

	def _sync(self):
		pickle.dump(self.data, self.fd)

# Only one database is allowed for now
# TODO: Set custom names for bot instances and
# allow to have one database per bot
database = HomeBotDatabase()
