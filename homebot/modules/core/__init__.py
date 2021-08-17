"""HomeBot core module."""

from homebot.core.mdlintf import (
	MODULE_TYPE_CORE,
	ModuleCommand,
	ModuleInterface,
	register_module,
)

from homebot.modules.core.main import (
	start,
	modules,
	enable,
	disable,
)

register_module(
	ModuleInterface(
		name = "core",
		version = "1.0.0",
		module_type = MODULE_TYPE_CORE,
		description = "Core functions of the bot",
		commands = {
			ModuleCommand(start, ['start', 'help']),
			ModuleCommand(modules, ['modules']),
			ModuleCommand(enable, ['enable']),
			ModuleCommand(disable, ['disable']),
		},
	)
)
