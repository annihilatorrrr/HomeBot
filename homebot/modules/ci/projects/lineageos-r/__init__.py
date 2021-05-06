"""LineageOS R CI project."""

from homebot.modules.ci.projects.lineageos import LineageOSProject

class Project(LineageOSProject):
	version = "18.1"
	android_version = "11"
