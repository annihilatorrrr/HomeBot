"""HomeBot XDA module."""

from homebot.core.mdlintf import (
	MODULE_TYPE_EXTERNAL,
	ModuleCommand,
	ModuleInterface,
	register_module,
)

from homebot.modules.xda.main import (
	xda,
)

register_module(
	ModuleInterface(
		name = "xda",
		version = "1.0",
		module_type = MODULE_TYPE_EXTERNAL,
		commands = {
			ModuleCommand(xda, ['xda']),
		},
	)
)
