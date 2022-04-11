from homebot.core.config import get_config
from homebot.modules.bridgey.pool import Pool

class Coordinator:
	"""This class is responsible for coordinating the message passing between platforms"""
	enabled = bool(get_config("bridgey.enabled", False))
	pools: dict[str, Pool] = {}
	if enabled:
		for pool_name in get_config("bridgey.pools", {}).keys():
			pools[pool_name] = Pool(pool_name)
