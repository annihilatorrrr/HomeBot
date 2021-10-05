"""HomeBot XDA module."""

from homebot.core.mdlintf import (
	ModuleInterface,
	register_module,
)

from homebot.modules.xda.main import (
	xda,
)

@register_module
class XdaModule(ModuleInterface):
	name = "xda"
	version = "1.0"
	commands = {
		xda: ["xda"],
	}
