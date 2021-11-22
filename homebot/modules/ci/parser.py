from argparse import ArgumentParser
from gettext import gettext
from telegram import Message

class CIParser(ArgumentParser):
	def set_output(self, reply_text: Message.reply_text):
		self.reply_text = reply_text

	def _print_message(self, message, file=None):
		if message:
			self.reply_text(message)

	def exit(self, status=0, message=None):
		if message:
			self._print_message(message)
		raise AssertionError(message)

	def error(self, message):
		self.print_usage()
		args = {'prog': self.prog, 'message': message}
		self.exit(2, gettext('%(prog)s: error: %(message)s\n') % args)
