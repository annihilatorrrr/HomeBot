"""HomeBot core module."""

from homebot import __version__
from homebot.core.modules_manager import ModuleBase
from homebot.lib.libadmin import user_is_admin
from telegram.ext import CallbackContext
from telegram.update import Update

class Module(ModuleBase):
	name = "core"
	description = "Core functions of the bot"
	version = "1.0.0"

	def start(update: Update, context: CallbackContext):
		update.message.reply_text("Hi! I'm HomeBot, and I'm alive\n"
								  f"Version {__version__}\n"
								  "To see all the available modules, type /modules")

	def modules(update: Update, context: CallbackContext):
		message = "Loaded modules:\n\n"
		modules = context.dispatcher.modules
		for module_name, module in modules.items():
			message += f"{module_name}\n"
			message += f"Status: {module.status}\n"
			message += f"Commands: {', '.join([command.name for command in module.commands])}\n\n"
		update.message.reply_text(message)

	def load(update: Update, context: CallbackContext):
		if not user_is_admin(update.message.from_user.id):
			update.message.reply_text("Error: You are not authorized to load modules")
			return

		if len(context.args) < 1:
			update.message.reply_text("Error: Module name not provided")
			return

		result = {}
		for module_name in context.args:
			if module_name == "core":
				text = "Error: You can't load module used for loading/unloading modules"
			else:
				try:
					context.dispatcher.load_module(module_name)
				except ModuleNotFoundError:
					text = "Error: Module not found"
				except AttributeError:
					text = "Module already loaded"
				else:
					text = "Module loaded"

			result[module_name] = text

		text = ""
		for module_name, status in result.items():
			text += f"{module_name}: {status}\n"
		update.message.reply_text(text)

	def unload(update: Update, context: CallbackContext):
		if not user_is_admin(update.message.from_user.id):
			update.message.reply_text("Error: You are not authorized to unload modules")
			return

		if len(context.args) < 1:
			update.message.reply_text("Error: Module name not provided")
			return

		result = {}
		for module_name in context.args:
			if module_name == "core":
				text = "Error: You can't unload module used for loading/unloading modules"
			else:
				try:
					context.dispatcher.unload_module(module_name)
				except ModuleNotFoundError:
					text = "Error: Module not found"
				except AttributeError:
					text = "Module already unloaded"
				else:
					text = "Module unloaded"

			result[module_name] = text

		text = ""
		for module_name, status in result.items():
			text += f"{module_name}: {status}\n"
		update.message.reply_text(text)

	commands = {
		start: ['start', 'help'],
		modules: ['modules'],
		load: ['load'],
		unload: ['unload']
	}
