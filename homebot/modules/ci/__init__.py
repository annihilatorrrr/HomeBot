"""HomeBot CI module."""

from homebot.core.mdlintf import (
	MODULE_TYPE_EXTERNAL,
	ModuleCommand,
	ModuleInterface,
	register_module,
)

from homebot.modules.ci.main import (
	ci,
)

register_module(
	ModuleInterface(
		name = "ci",
		version = "1.0",
		module_type = MODULE_TYPE_EXTERNAL,
		commands = {
			ModuleCommand(ci, ['ci']),
		},
	)
)
