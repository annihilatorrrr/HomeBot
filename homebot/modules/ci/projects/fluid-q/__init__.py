"""Fluid Q CI project."""

from homebot.modules.ci.projects.aosp.project import AOSPProject

class Project(AOSPProject):
	name = "Fluid"
	version = "10.0"
	android_version = "10"
	category = "ROMs"
	lunch_prefix = "fluid"
	lunch_suffix = "userdebug"
	build_target = "bacon"
	artifacts = "Fluid-*.zip"
