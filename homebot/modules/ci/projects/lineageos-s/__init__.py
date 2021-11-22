"""LineageOS S CI project."""

from homebot.lib.libaosp.project import AOSPProject

class Project(AOSPProject):
	name = "LineageOS"
	version = "19.0"
	android_version = "12"
	zip_name = "lineage-*.zip"
	lunch_prefix = "lineage"
	date_regex = "lineage-[0-9.]+-(.+?)-.*.zip"
