"""HomeBot weather module."""

from homebot.core.logging import LOGE
from homebot.core.modules_manager import ModuleBase
from homebot.lib.libweather import Weather
from telegram.ext import CallbackContext
from telegram.update import Update

class Module(ModuleBase):
	name = "weather"
	description = "Get the weather of a city"
	version = "1.0.0"

	def weather(update: Update, context: CallbackContext):
		try:
			city = update.message.text.split(' ', 1)[1]
		except IndexError:
			update.message.reply_text("City not provided")
			return
		try:
			weather = Weather()
		except AssertionError:
			update.message.reply_text("OpenWeatherMap API key not specified\n"
									  "Ask the bot hoster to configure it")
			LOGE("OpenWeatherMap API key not specified, get it at https://home.openweathermap.org/api_keys")
			return
		try:
			response = weather.current_weather(city)
		except ConnectionError as err:
			update.message.reply_text(err.strerror)
			return
		city_name = response["name"]
		city_country = response["sys"]["country"]
		city_lat = response["coord"]["lat"]
		city_lon = response["coord"]["lon"]
		weather_type = response["weather"][0]["main"]
		weather_type_description = response["weather"][0]["description"]
		temp = response["main"]["temp"]
		temp_min = response["main"]["temp_min"]
		temp_max = response["main"]["temp_max"]
		humidity = response["main"]["humidity"]
		wind_speed = response["wind"]["speed"]
		update.message.reply_text(
			f"Current weather for {city_name}, {city_country} ({city_lat}, {city_lon}):\n"
			f"Weather: {weather_type} ({weather_type_description})\n"
			f"Temperature: {temp}{weather.temp_unit} (Min: {temp_min}{weather.temp_unit} Max: {temp_max}{weather.temp_unit})\n"
			f"Humidity: {humidity}%\n"
			f"Wind: {wind_speed}{weather.wind_unit}"
		)

	commands = {
		weather: ['weather']
	}
