"""HomeBot shell module."""

from homebot.core.mdlintf import (
	ModuleInterface,
	register_module,
)

from homebot.modules.shell.main import (
	shell,
)

@register_module
class Shell(ModuleInterface):
	name = "shell"
	version = "1.0"
	core: True
	commands = {
		shell: ["shell"],
	}
