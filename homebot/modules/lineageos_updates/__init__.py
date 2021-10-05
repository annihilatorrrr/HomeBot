"""HomeBot LineageOS updates module."""

from homebot.core.mdlintf import (
	ModuleInterface,
	register_module,
)

from homebot.modules.lineageos_updates.main import (
	add_user,
	remove_user,
	lineageos_updates,
)

@register_module
class LineageosUpdatesModule(ModuleInterface):
	name = "lineageos_updater"
	version = "1.0"
	add_user = add_user
	remove_user = remove_user
	commands = {
		lineageos_updates: ["lineageos_updates"],
	}
