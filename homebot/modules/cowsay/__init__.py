"""HomeBot cowsay module."""

from homebot.core.mdlintf import (
	MODULE_TYPE_EXTERNAL,
	ModuleCommand,
	ModuleInterface,
	register_module,
)

from homebot.modules.cowsay.main import (
	cowsay,
)

register_module(
	ModuleInterface(
		name = "cowsay",
		version = "1.0.0",
		module_type = MODULE_TYPE_EXTERNAL,
		description = "Moo",
		commands = {
			ModuleCommand(cowsay, ['cowsay']),
		},
		ioctl = None,
	)
)
