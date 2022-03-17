"""LineageOS utils library."""

from homebot.lib.libandroid import AndroidVersion

GITHUB_ORG = "https://github.com/LineageOS"

LINEAGEOS_TO_ANDROID_VERSION = {
    "13.0": AndroidVersion.M,
    "14.1": AndroidVersion.N,
    "15.1": AndroidVersion.O,
	"16.0": AndroidVersion.P,
	"17.1": AndroidVersion.Q,
	"18.1": AndroidVersion.R,
	"19.1": AndroidVersion.S,
}
