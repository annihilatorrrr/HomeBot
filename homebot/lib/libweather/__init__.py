"""OpenWeatherMap implementation library"""

from homebot import get_config
import requests

DATA_VERSION = "2.5"

STANDARD_URL = f"https://api.openweathermap.org/data/{DATA_VERSION}"
PRO_URL = f"https://pro.openweathermap.org/data/{DATA_VERSION}"

CURRENT_WEATHER_URL = f"{STANDARD_URL}/weather"
HOURLY_FORECAST_URL = f"{STANDARD_URL}/forecast/hourly"
ONE_CALL_URL = f"{STANDARD_URL}/onecall"
DAILY_FORECAST_URL = f"{STANDARD_URL}/forecast/daily"
CLIMATIC_FORECAST_URL = f"{STANDARD_URL}/forecast/climate"
BULK_SNAPSHOT_URL = f"http://bulk.openweathermap.org/snapshot"
BULK_ARCHIVE_URL = f"http://bulk.openweathermap.org/archive"
SOLAR_RADIATION_URL = f"{STANDARD_URL}/solar_radiation"
FORECAST_URL = f"{STANDARD_URL}/forecast"
ROADRISK_URL = f"{STANDARD_URL}/roadrisk"

TEMP_UNITS = {
	"imperial": "F",
	"metric": "C"
}

WIND_UNITS = {
	"imperial": "mph",
	"metric": "km/h"
}

class Weather:
	def __init__(self):
		self.api_key = get_config("WEATHER_API_KEY", None)
		if self.api_key is None:
			raise AssertionError("An API key is needed")
		self.base_unit = get_config("WEATHER_TEMP_UNIT", "metric")
		self.temp_unit = TEMP_UNITS.get(self.base_unit, "K")
		self.wind_unit = WIND_UNITS.get(self.base_unit, "km/h")

	def get_data(self, url: str, **kwargs) -> dict:
		params = {
			"appid": self.api_key,
			"units": self.base_unit,
		}
		params.update(kwargs)

		response = requests.get(url=url, params=params).json()
		if response["cod"] != 200:
			raise ConnectionError(f"Invalid response: {response['message']}")
		return response

	def current_weather(self, q: str):
		"""https://openweathermap.org/current"""
		return self.get_data(CURRENT_WEATHER_URL, q=q)

	def hourly_forecast(self, q: str):
		"""https://openweathermap.org/api/hourly-forecast"""
		return self.get_data(HOURLY_FORECAST_URL, q=q)

	def one_call(self, lat: str, lon: str):
		"""https://openweathermap.org/api/one-call-api"""
		return self.get_data(ONE_CALL_URL, lat=lat, lon=lon)

	def daily_forecast(self, q: str):
		"""https://openweathermap.org/forecast16"""
		return self.get_data(DAILY_FORECAST_URL, q=q)

	def climatic_forecast(self, q: str):
		"""https://openweathermap.org/api/forecast30"""
		return self.get_data(CLIMATIC_FORECAST_URL, q=q)

	def bulk_snapshot(self, file_name: str):
		"""https://openweathermap.org/bulk"""
		return self.get_data(f"{BULK_SNAPSHOT_URL}/{file_name}")

	def bulk_archive(self, file_name: str):
		"""https://openweathermap.org/bulk"""
		return self.get_data(f"{BULK_ARCHIVE_URL}/{file_name}")
	
	def solar_radiation(self, lat: str, lon: str):
		"""https://openweathermap.org/api/solar-radiation"""
		return self.get_data(SOLAR_RADIATION_URL, lat=lat, lon=lon)

	def forecast(self, q: str):
		"""https://openweathermap.org/forecast5"""
		return self.get_data(FORECAST_URL, q=q)

	def roadrisk(self):
		"""https://openweathermap.org/api/road-risk"""
		return self.get_data(ROADRISK_URL)
