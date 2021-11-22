"""Fluid R CI project."""

from homebot.lib.libaosp.project import AOSPProject

class Project(AOSPProject):
	name = "Fluid"
	version = "1.x"
	android_version = "11"
	zip_name = "Fluid-*.zip"
	lunch_prefix = "fluid"
	date_regex = "Fluid-[0-9.]+-[a-zA-Z]+-[a-zA-Z]+-.+-([0-9]+).*.zip"
