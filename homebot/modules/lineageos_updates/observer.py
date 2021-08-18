from homebot.core.config import get_config
from homebot.modules.lineageos_updates.device_data import DeviceData
from homebot.modules.lineageos_updates.poster import posters
import requests
from threading import Event, Thread
from time import sleep, time

API_URL = "https://download.lineageos.org/api/v1/{device}/nightly/1"

class Observer:
	def __init__(self):
		self.devices = get_config("lineageos_updater.devices", [])
		self.last_device_update = {}

		for device in self.devices:
			self.last_device_update[device] = int(time())

		self.event = Event()
		if get_config("lineageos_updater.enable", False) and self.devices:
			self.event.set()

		self.thread = Thread(target=self.daemon, name="LineageOS updater observer")
		self.thread.start()

	def daemon(self):
		while True:
			self.event.wait()
			for device in self.devices:
				api_url = API_URL.format(device=device)
				response = requests.get(url=api_url).json()["response"]
				if not response:
					continue

				last_update = response[-1]

				if last_update["datetime"] <= self.last_device_update[device]:
					continue
				self.last_device_update[device] = last_update["datetime"]

				device_data = DeviceData(device)

				for poster in posters.values():
					poster.post(device_data, last_update["datetime"], last_update["version"])

			# Wait 30 minutes
			sleep(30 * 60)

observer = Observer()
