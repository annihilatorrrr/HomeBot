"""Module interface library."""

from homebot.core.mdlintf import ModuleInterface
from homebot.core.mdlintf import register_module as _register_module

def register_module(mdlintf: ModuleInterface):
	return _register_module(mdlintf)
