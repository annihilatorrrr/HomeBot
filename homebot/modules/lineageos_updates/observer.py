from datetime import datetime
from homebot.core.config import get_config
from homebot.lib.liblineage.ota import get_nightlies
from homebot.lib.liblogging import LOGE, LOGI
from threading import Event, Thread
from time import sleep

class Observer:
	def __init__(self):
		self.devices = get_config("lineageos_updates.devices", [])
		self.last_device_post = {}
		self.posters = {}

		now = datetime.now()
		for device in self.devices:
			self.last_device_post[device] = now

		self.event = Event()
		if get_config("lineageos_updates.enable", False) and self.devices:
			self.event.set()

		self.thread = Thread(target=self.daemon, name="LineageOS updates observer", daemon=True)
		self.thread.start()

	def daemon(self):
		while True:
			self.event.wait()
			for device in self.devices:
				try:
					response = get_nightlies(device)
				except Exception:
					response = []

				if not response:
					continue

				last_update = response[-1]

				build_date = last_update.datetime
				if build_date <= self.last_device_post[device]:
					continue

				self.last_device_post[device] = build_date

				for poster in self.posters.values():
					try:
						poster.post(device, last_update)
					except Exception:
						LOGE(f"Failed to post {device} {build_date} build")
					else:
						LOGI(f"Build {device} {build_date} posted successfully")

			# Wait 10 minutes
			sleep(10 * 60)
