#
# Module Interface core
#

# TODO: Remove with Python 3.10
from __future__ import annotations

from homebot.core.error_handler import format_exception
from homebot.core.logging import LOGD, LOGE, LOGI, LOGW
from importlib import import_module
from pathlib import Path
from pkgutil import iter_modules
from telegram.bot import Bot
from telegram.ext import CallbackContext, CommandHandler
from telegram.update import Update
from threading import Lock
from typing import Any, Callable

def register_modules(modules_path: Path):
	"""Import all the modules and let them execute register_module()."""
	for module_name in [name for _, name, _ in iter_modules([str(modules_path)])]:
		try:
			import_module(f'homebot.modules.{module_name}')
		except Exception as e:
			LOGE(f"Error importing module {module_name}:\n"
			     f"{format_exception(e)}")

#
# Module IOCTL
#
class IOCTLData:
	"""
	Class used to exchange data with IOCTL calls
	"""
	def __init__(self, ioctl: int, data: Any):
		"""
		Prepare IOCTL data.
		"""
		self.ioctl = ioctl
		self.data = data
		self.returndata = None
		self.lock = Lock()

	def get_returndata(self):
		"""
		Retrieve return data
		"""
		with self.lock:
			return self.returndata

	def set_returndata(self, data: Any):
		"""
		Set return data
		"""
		with self.lock:
			self.returndata = data

# IOCTL return value
(
	# IOCTL returned successfully
	MODULE_IOCTL_RESULT_OK,
	# Requested module isn't registered
	MODULE_IOCTL_RESULT_MODULE_NOT_FOUND,
	# The module doesn't support IOCTL
	MODULE_IOCTL_RESULT_NO_IOCTL,
	# IOCTL value not supported
	MODULE_IOCTL_RESULT_NOT_SUPPORTED,
	# Module-specific error
	MODULE_IOCTL_RESULT_MODULE_ERROR,
) = range(5)

def mdlintf_ioctl(module_name: str, data: IOCTLData):
	"""
	Perform a IOCTL call.

	If everything went ok, this function will return MODULE_IOCTL_RESULT_OK
	and returned data will be in data instance,
	else refer to MODULE_IOCTL_RESULT_* and module specific constants
	"""
	module = get_module(module_name)
	if module is None:
		return MODULE_IOCTL_RESULT_MODULE_NOT_FOUND

	return module.ioctl(data)

def get_command_handler(module, commands, function):
	new_function = lambda update, context: function(module, update, context)
	new_function.__name__ = function.__name__
	return CommandHandler(commands, new_function, run_async=True)

class ModuleInterface:
	name: str = "none"
	version: str = "0.0"
	core: bool = False
	module_init: Callable[[ModuleInterface], None] = lambda self: None
	add_user: Callable[[ModuleInterface, Bot], None] = lambda self, bot: None
	remove_user: Callable[[ModuleInterface, Bot], None] = lambda self, bot: None
	commands: dict[Callable[[ModuleInterface, Update, CallbackContext], None], list[str]] = []
	ioctl: Callable[[ModuleInterface, IOCTLData], int] = lambda self, data: MODULE_IOCTL_RESULT_NO_IOCTL

	def __init__(self):
		self.handlers = [
			get_command_handler(self, commands, function)
			for function, commands in self.commands.items()
		]

		self.module_init()

#
# Module Binder IPC
#
_mdlbinder: dict[str, ModuleInterface] = {}
_mdlbinder_lock = Lock()

def get_all_modules_list():
	with _mdlbinder_lock:
		return _mdlbinder.keys()

def get_module(module_name: str):
	with _mdlbinder_lock:
		module_found = module_name in _mdlbinder

	if not module_found:
		# New module added while running? Try to import it
		try:
			import_module(f'homebot.modules.{module_name}')
		except Exception:
			LOGD(f"Tried to import module {module_name} but failed")

	with _mdlbinder_lock:
		if module_name in _mdlbinder:
			return _mdlbinder[module_name]
		else:
			LOGW(f'Module {module_name} not found')
			return None

def register_module(mdlintf: ModuleInterface):
	with _mdlbinder_lock:
		name = mdlintf.name
		if name in _mdlbinder:
			LOGW(f'Replacing already registered module "{mdlintf.name}" with a new instance, '
							f'old ID: {id(_mdlbinder[name])}, new ID: {id(mdlintf)}')
			del _mdlbinder[name]

		_mdlbinder[name] = mdlintf()

		LOGI(f'Registered module "{name}" with ID {id(_mdlbinder[name])}')

		return mdlintf
