"""HomeBot LineageOS updates module."""

from homebot.core.mdlintf import (
	ModuleInterface,
	register_module,
)

from homebot.modules.lineageos_updates.main import (
	module_init,
	add_user,
	remove_user,
	lineageos_updates,
)

@register_module
class LineageosUpdatesModule(ModuleInterface):
	name = "lineageos_updates"
	version = "1.0"
	module_init = module_init
	add_user = add_user
	remove_user = remove_user
	commands = {
		lineageos_updates: ["lineageos_updates"],
	}
