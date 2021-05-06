"""RevengeOS common CI project."""

from homebot.modules.ci.projects.aosp.project import AOSPProject

class RevengeOSProject(AOSPProject):
	name = "RevengeOS"
	category = "ROMs"
	lunch_prefix = "revengeos"
	lunch_suffix = "userdebug"
	build_target = "bacon"
	artifacts = "RevengeOS-*.zip"
