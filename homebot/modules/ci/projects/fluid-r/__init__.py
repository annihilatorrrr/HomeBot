"""Fluid R CI project."""

from homebot.modules.ci.projects.aosp.project import AOSPProject

class Project(AOSPProject):
	name = "Fluid"
	version = "11.0"
	android_version = "11"
	category = "ROMs"
	lunch_prefix = "fluid"
	lunch_suffix = "userdebug"
	build_target = "bacon"
	artifacts = "Fluid-*.zip"
