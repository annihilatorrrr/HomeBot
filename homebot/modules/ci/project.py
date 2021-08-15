from telegram.ext import CallbackContext
from telegram.update import Update

class ProjectBase:
	name: str

	def __init__(self, update: Update, context: CallbackContext, args: list[str]):
		"""Initialize the project class."""
		self.update = update
		self.context = context
		self.args = args

	def build(self):
		pass

	def get_info(self):
		return (f"{self.name}\n"
		        f"Arguments: {' '.join(self.args)}\n"
		        f"Started by: {self.update.effective_user.name}\n")
