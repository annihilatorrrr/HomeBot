from homebot.core.error_handler import error_handler
from homebot.core.mdlintf import mdlbinder
from homebot.lib.libexception import format_exception
from homebot.lib.liblogging import LOGE, LOGI
from os import execl
from signal import SIGTERM
import sys
from telegram.ext import ContextTypes, Updater
from threading import Lock

class _ModuleStatus:
	def __init__(self, status: int, string: str):
		self.status = status
		self.string = string

	def __int__(self):
		return self.status

	def __str__(self) -> str:
		return self.string

class ModuleStatus(_ModuleStatus):
	"""
	Module status.

	This class indicates the status of a HomeBot module for the bot.
	Can be casted to int and str.
	"""
	(
		_DISABLED,
		_ENABLED,
		_ENABLING,
		_DISABLING,
		_ERROR,
	) = range(5)

	DISABLED = _ModuleStatus(_DISABLED, "Disabled")
	ENABLED = _ModuleStatus(_ENABLED, "Enabled")
	ENABLING = _ModuleStatus(_ENABLING, "Enabling")
	DISABLING = _ModuleStatus(_DISABLING, "Disabling")
	ERROR = _ModuleStatus(_ERROR, "Error")

BOT_DATA_HOMEBOT = "homebot"

class HomeBot(Updater):
	"""
	Main HomeBot class.

	It is a subclass of telegram.ext.Updater with the addition of:
	- A basic error handler that send the traceback to
	  the user and to the console
	- mdlintf modules loading on init (each module's handlers will have a shared unique group)
	"""
	def __init__(self, token: str):
		"""Initialize the bot."""
		context_types = ContextTypes(bot_data=lambda: {BOT_DATA_HOMEBOT: self})
		super().__init__(token=token, context_types=context_types)

		self.dispatcher.add_error_handler(error_handler, True)

		self.modules: dict[str, ModuleStatus] = {}
		self.modules_group: list[str] = []
		self.modules_lock = Lock()

		for module_name in mdlbinder.get_registered_interfaces():
			self.enable_module(module_name, False)

		self.set_my_commands()

	def enable_module(self, module_name: str, set_my_commands: bool = True):
		"""
		Enable a provided module and add its command handler
		to the bot's dispatcher.
		"""
		LOGI(f"Enabling module {module_name}")

		module = mdlbinder.get_interface(module_name)

		with self.modules_lock:
			if not module_name in self.modules:
				self.modules[module_name] = ModuleStatus.DISABLED

			if self.modules[module_name] == ModuleStatus.ENABLED:
				raise AttributeError("Module is already enabled")

			self.modules[module_name] = ModuleStatus.ENABLING

			try:
				if not module_name in self.modules_group:
					self.modules_group.append(module_name)
				module_group = self.modules_group.index(module_name)

				for handler in module.handlers:
					self.dispatcher.add_handler(handler, module_group)
				module.add_user(self.dispatcher.bot)
			except Exception as e:
				LOGE(f"Failed to add handler for module {module_name}\n"
				     f"{format_exception(e)}")
				self.modules[module_name] = ModuleStatus.ERROR
			else:
				self.modules[module_name] = ModuleStatus.ENABLED
				LOGI(f"Module {module_name} enabled")

		if set_my_commands:
			self.set_my_commands()

	def disable_module(self, module_name: str, set_my_commands: bool = True):
		"""
		Disable a provided module and remove its command handler
		from the bot's dispatcher.
		"""
		LOGI(f"Disabling module {module_name}")

		module = mdlbinder.get_interface(module_name)

		with self.modules_lock:
			if not module_name in self.modules:
				self.modules[module_name] = ModuleStatus.DISABLED

			if self.modules[module_name] == ModuleStatus.DISABLED:
				raise AttributeError("Module is already disabled")

			self.modules[module_name] = ModuleStatus.DISABLING

			try:
				module_group = self.modules_group.index(module_name)

				for handler in module.handlers:
					self.dispatcher.remove_handler(handler, module_group)
				module.remove_user(self.dispatcher.bot)
			except Exception as e:
				LOGE(f"Failed to remove handler for module {module_name}\n"
				     f"{format_exception(e)}")
				self.modules[module_name] = ModuleStatus.ERROR
			else:
				self.modules[module_name] = ModuleStatus.DISABLED
				LOGI(f"Module {module_name} disabled")

		if set_my_commands:
			self.set_my_commands()

	def set_my_commands(self):
		"""Set the bot's own commands based on the enabled handlers."""
		commands = []

		with self.modules_lock:
			for module_name in self.modules:
				if not (self.modules[module_name] is ModuleStatus.ENABLED):
					continue

				module = mdlbinder.get_interface(module_name)
				commands.extend(module.commands_help)

		self.bot.set_my_commands(commands)

	def restart(self):
		"""Restart the bot."""
		LOGI("Restarting")

		execl(sys.executable, sys.executable, *["-m", "homebot"])

	def shutdown(self):
		"""Shutdown the bot."""
		LOGI("Shutting down")

		self._signal_handler(SIGTERM, None)
