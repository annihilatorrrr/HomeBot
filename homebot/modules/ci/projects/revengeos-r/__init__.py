"""RevengeOS R CI project."""

from homebot.modules.ci.projects.aosp.project import AOSPProject

class Project(AOSPProject):
	name = "RevengeOS"
	version = "4.0"
	android_version = "11"
	category = "ROMs"
	lunch_prefix = "revengeos"
	lunch_suffix = "userdebug"
	build_target = "bacon"
	artifacts = "RevengeOS-*.zip"
