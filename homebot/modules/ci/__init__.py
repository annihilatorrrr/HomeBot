"""HomeBot CI module."""

from homebot.core.mdlintf import (
	ModuleInterface,
	register_module,
)

from homebot.modules.ci.main import (
	ci,
)

@register_module
class CiModule(ModuleInterface):
	name = "ci"
	version = "1.0"
	commands = {
		ci: ["ci"],
	}
