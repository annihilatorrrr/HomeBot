"""SHRP P CI project."""

from homebot.modules.ci.projects.aosp.project import AOSPProject

class Project(AOSPProject):
	name = "SHRP"
	version = "P"
	android_version = "9"
	category = "Recoveries"
	lunch_prefix = "omni"
	lunch_suffix = "userdebug"
	build_target = "recoveryimage"
	artifacts = "SHRP-*.zip"
