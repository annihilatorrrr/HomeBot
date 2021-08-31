"""SHRP Q CI project."""

from homebot.modules.ci.projects.aosp.project import AOSPProject

class Project(AOSPProject):
	name = "SHRP"
	version = "Q"
	android_version = "10"
	category = "Recoveries"
	lunch_prefix = "omni"
	lunch_suffix = "userdebug"
	build_target = "recoveryimage"
	artifacts = "SHRP-*.zip"
