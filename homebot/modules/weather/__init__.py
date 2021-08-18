"""HomeBot weather module."""

from homebot.core.mdlintf import (
	MODULE_TYPE_EXTERNAL,
	ModuleCommand,
	ModuleInterface,
	register_module,
)

from homebot.modules.weather.main import (
	weather,
)

register_module(
	ModuleInterface(
		name = "weather",
		version = "1.0.0",
		module_type = MODULE_TYPE_EXTERNAL,
		commands = {
			ModuleCommand(weather, ['weather'])
		},
	)
)
