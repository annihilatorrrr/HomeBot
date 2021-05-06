"""Fluid common CI project."""

from homebot.modules.ci.projects.aosp.project import AOSPProject

class FluidProject(AOSPProject):
	name = "Fluid"
	category = "ROMs"
	lunch_prefix = "fluid"
	lunch_suffix = "userdebug"
	build_target = "bacon"
	artifacts = "Fluid-*.zip"
