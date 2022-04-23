from datetime import datetime
from homebot.core.config import get_config
from sebaubuntu_libs.libexception import format_exception
from sebaubuntu_libs.liblineage.hudson import get_lineage_build_targets
from sebaubuntu_libs.liblineage.ota import get_nightlies
from sebaubuntu_libs.liblogging import LOGE, LOGI
from threading import Event, Thread
from time import sleep

class Observer:
	def __init__(self):
		self.last_device_post = {}
		self.posters = {}

		now = datetime.now()
		self.set_start_date(now)

		self.event = Event()
		if get_config("lineageos_updates.enable", False):
			self.event.set()

		self.thread = Thread(target=self.daemon, name="LineageOS updates observer", daemon=True)
		self.thread.start()

	def daemon(self):
		while True:
			self.event.wait()
			for device in [build_target.device for build_target in get_lineage_build_targets()]:
				try:
					response = get_nightlies(device)
				except Exception:
					response = []

				if not response:
					LOGI(f"No updates for {device}")
					continue

				last_update = response[-1]

				build_date = last_update.datetime
				if device in self.last_device_post and build_date <= self.last_device_post[device]:
					continue

				self.last_device_post[device] = build_date

				for poster in self.posters.values():
					try:
						poster.post(device, last_update)
					except Exception as e:
						LOGE(f"Failed to post {device} {build_date} build\n"
						     f"{format_exception(e)}")

			# Wait 10 minutes
			sleep(10 * 60)

	def set_start_date(self, date: datetime):
		for device in [build_target.device for build_target in get_lineage_build_targets()]:
			self.last_device_post[device] = date
