"""LineageOS R CI project."""

from homebot.lib.libaosp.project import AOSPProject

class Project(AOSPProject):
	name = "LineageOS"
	version = "18.1"
	android_version = "11"
	zip_name = "lineage-*.zip"
	lunch_prefix = "lineage"
	date_regex = "lineage-[0-9.]+-(.+?)-.*.zip"
