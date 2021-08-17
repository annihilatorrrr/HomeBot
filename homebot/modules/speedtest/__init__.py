"""HomeBot speedtest module."""

from homebot.core.mdlintf import (
	MODULE_TYPE_EXTERNAL,
	ModuleCommand,
	ModuleInterface,
	register_module,
)

from homebot.modules.speedtest.main import (
	speedtest,
)

register_module(
	ModuleInterface(
		name = "speedtest",
		version = "1.0.0",
		module_type = MODULE_TYPE_EXTERNAL,
		description = "Do a speedtest",
		commands = {
			ModuleCommand(speedtest, ['speedtest']),
		},
	)
)
