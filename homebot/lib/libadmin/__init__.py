"""Admin utils library."""

from homebot import get_config
from homebot.core.logging import LOGI

def user_is_admin(user_id):
	"""
	Check if the given user ID is in the list
	of the approved user IDs.
	"""
	if str(user_id) not in get_config("CI_APPROVED_USER_IDS").split():
		LOGI(f"Access denied to user {user_id}")
		return False

	LOGI(f"Access granted to user {user_id}")
	return True
