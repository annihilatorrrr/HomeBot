#
# Module Interface core
#

from homebot.core.error_handler import format_exception
from homebot.core.logging import LOGD, LOGE, LOGI, LOGW
from importlib import import_module
from pathlib import Path
from pkgutil import iter_modules
from telegram.bot import Bot
from telegram.ext import CommandHandler, CallbackContext
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

# Module type
(
	MODULE_TYPE_CORE,
	MODULE_TYPE_EXTERNAL,
) = range(2)

MODULE_TYPE_MESSAGE = {
	MODULE_TYPE_CORE: "Core",
	MODULE_TYPE_EXTERNAL: "External",
}

class ModuleCommand:
	"""
	A class representing a HomeBot module command
	"""
	def __init__(self, function: Callable[[Update, CallbackContext], Any], commands: list) -> None:
		"""
		Initialize the command class.
		"""
		self.name = function.__name__
		self.handler = CommandHandler(commands, function, run_async=True)

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

class ModuleInterface:
	def __init__(self,
				 name: str,
				 version: str,
				 module_type: int,
				 add_user: Callable[[Bot], Any] = lambda bot: None,
				 remove_user: Callable[[Bot], Any] = lambda bot: None,
				 commands: list[ModuleCommand] = [],
				 ioctl: Callable[[IOCTLData], int] = lambda data: MODULE_IOCTL_RESULT_NO_IOCTL,
				):
		"""Initialize the interface."""
		self.name = name
		self.version = version
		self.type = module_type
		self.add_user = add_user
		self.remove_user = remove_user
		self.commands = commands
		self.ioctl = ioctl

#
# Module Binder IPC
#
_mdlbinder = {}
_mdlbinder_lock = Lock()

_mdlbinder: dict[str, ModuleInterface]

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

		_mdlbinder[name] = mdlintf

		LOGI(f'Registered module "{name}" with ID {id(_mdlbinder[name])}')
