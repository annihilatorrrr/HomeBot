from homebot.core.error_handler import error_handler
from homebot.core.logging import LOGE, LOGI
from homebot.core.mdlintf import get_all_modules_list, get_module
from telegram.ext import Dispatcher, Updater
from threading import Lock
from types import MethodType

# Module status
(
	MODULE_STATUS_DISABLED,
	MODULE_STATUS_ENABLED,
	MODULE_STATUS_ENABLING,
	MODULE_STATUS_DISABLING,
	MODULE_STATUS_ERROR,
) = range(5)

MODULE_STATUS_MESSAGE = {
	MODULE_STATUS_DISABLED: "Disabled",
	MODULE_STATUS_ENABLED: "Enabled",
	MODULE_STATUS_ENABLING: "Enabling",
	MODULE_STATUS_DISABLING: "Disabling",
	MODULE_STATUS_ERROR: "Error",
}

def enable_module(self: Dispatcher, module_name: str):
	"""
	Load a provided module and add its command handler
	to the bot's dispatcher.
	"""
	LOGI(f"Loading module {module_name}")

	module = get_module(module_name)
	if module is None:
		raise ModuleNotFoundError(f"Module {module_name} not found")

	with self.modules_status_lock:
		if not module_name in self.modules_status:
			self.modules_status[module_name] = MODULE_STATUS_DISABLED

		if self.modules_status[module_name] == MODULE_STATUS_ENABLED:
			raise AttributeError("Module is already enabled")

		self.modules_status[module_name] = MODULE_STATUS_ENABLING

		try:
			for command in module.commands:
				self.add_handler(command.handler)
			module.add_user(self.bot)
		except:
			LOGE(f"Failed to add handler for module {module_name}")
			self.modules_status[module_name] = MODULE_STATUS_ERROR

		self.modules_status[module_name] = MODULE_STATUS_ENABLED

	LOGI(f"Module {module_name} enabled")

def disable_module(self: Dispatcher, module_name: str):
	"""
	Unload a provided module and remove its command handler
	from the bot's dispatcher.
	"""
	LOGI(f"Loading module {module_name}")

	module = get_module(module_name)
	if module is None:
		raise ModuleNotFoundError(f"Module {module_name} not found")

	with self.modules_status_lock:
		if not module_name in self.modules_status:
			self.modules_status[module_name] = MODULE_STATUS_DISABLED

		if self.modules_status[module_name] == MODULE_STATUS_DISABLED:
			raise AttributeError("Module is already disabled")

		self.modules_status[module_name] = MODULE_STATUS_DISABLING

		try:
			for command in module.commands:
				self.add_handler(command.handler)
			module.remove_user(self.bot)
		except:
			LOGE(f"Failed to add handler for module {module_name}")
			self.modules_status[module_name] = MODULE_STATUS_ERROR

		self.modules_status[module_name] = MODULE_STATUS_DISABLED

	LOGI(f"Module {module_name} disabled")

class HomeBot(Updater):
	def __init__(self, token: str):
		super().__init__(token=token)

		self.dispatcher.add_error_handler(error_handler, True)

		self.dispatcher.modules_status = {}
		self.dispatcher.modules_status_lock = Lock()

		self.dispatcher.enable_module = MethodType(enable_module, self.dispatcher)
		self.dispatcher.disable_module = MethodType(disable_module, self.dispatcher)

		for module_name in get_all_modules_list():
			self.dispatcher.enable_module(module_name)
