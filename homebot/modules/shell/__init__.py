"""HomeBot shell module."""

from homebot.core.mdlintf import (
	MODULE_TYPE_CORE,
	ModuleCommand,
	ModuleInterface,
	register_module,
)

from homebot.modules.shell.main import (
	shell,
)

register_module(
	ModuleInterface(
		name = "shell",
		version = "1.0.0",
		module_type = MODULE_TYPE_CORE,
		commands = {
			ModuleCommand(shell, ['shell']),
		},
	)
)
