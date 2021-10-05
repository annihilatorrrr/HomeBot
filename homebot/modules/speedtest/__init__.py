"""HomeBot speedtest module."""

from homebot.core.mdlintf import (
	ModuleInterface,
	register_module,
)

from homebot.modules.speedtest.main import (
	speedtest,
)

@register_module
class SpeedtestModule(ModuleInterface):
	name = "speedtest"
	version = "1.0"
	commands = {
		speedtest: ["speedtest"],
	}
