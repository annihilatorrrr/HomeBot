"""HomeBot core module."""

from homebot.core.mdlintf import (
	ModuleInterface,
	register_module,
)

from homebot.modules.core.main import (
	start,
	modules,
	enable,
	disable,
)

@register_module
class CoreModule(ModuleInterface):
	name = "core"
	version = "1.0"
	core: True
	commands = {
		start: ["start", "help"],
		modules: ["modules"],
		enable: ["enable"],
		disable: ["disable"],
	}
