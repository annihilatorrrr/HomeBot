"""HomeBot LineageOS updates module."""

from homebot.core.mdlintf import (
	MODULE_TYPE_EXTERNAL,
	ModuleCommand,
	ModuleInterface,
	register_module,
)

from homebot.modules.lineageos_updates.main import (
	add_user,
	remove_user,
)

register_module(
	ModuleInterface(
		name = "lineageos_updater",
		version = "1.0.0",
		module_type = MODULE_TYPE_EXTERNAL,
		add_user = add_user,
		remove_user = remove_user,
	)
)
