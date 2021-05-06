"""SHRP common CI project."""

from homebot.modules.ci.projects.aosp.project import AOSPProject

class SHRPProject(AOSPProject):
	name = "SHRP"
	category = "Recoveries"
	lunch_prefix = "omni"
	lunch_suffix = "userdebug"
	build_target = "recoveryimage"
	artifacts = "SHRP-*.zip"
