"""LineageOS common CI project."""

from homebot.modules.ci.projects.aosp.project import AOSPProject

class LineageOSProject(AOSPProject):
	name = "LineageOS"
	category = "ROMs"
	lunch_prefix = "lineage"
	lunch_suffix = "userdebug"
	build_target = "bacon"
	artifacts = "lineage-*.zip"
