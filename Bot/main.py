import os
import datetime
import requests
import math
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor 

#для защиты от спама
PROXY_URL="http://proxy.server:3128"
bot = Bot(token='6058928493:AAHQ5s7q3opedxwqIXBJytcW3MpMN0OyBn0')
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
	await message.reply("Привіт! Напиши назву міста і я надішлю прогноз погоди")

@dp.message_handler()
async def get_weather(message: types.Message):
	try:
		name_city = message.text
		response = requests.get(
			f"http://api.openweathermap.org/data/2.5/weather?q={name_city}&lang=uk&units=metric&limit=5&appid=92fce17d278e5732b500290984a6dc39"
        )
		data = response.json()

		city = data["name"]
		cur_temp = data["main"]["temp"]
		humidity = data["main"]["humidity"]
		pressure = data["main"]["pressure"]
		wind = data["wind"]["speed"]
		sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
		sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
		length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(data["sys"]["sunrise"])

		code_to_smile = {
			"Clear": "Сонячно \U00002600",
			"Clouds": "Хмарно \U00002601",
			"Rain": "Дощ \U00002614",
			"Drizzle": "Мряка \U00002614",
			"Thunderstorm": "Гроза \U000026A1",
			"Snow": "Сніг \U0001F328",
			"Mist": "Туман \U0001F32B"
		}
		# получаем значение погоды
		weather_description = data["weather"][0]["main"]

		if weather_description in code_to_smile:
			wd = code_to_smile[weather_description]
		else:
			wd = "Подивись у вікно, бо я не розумію яка погода"

		await message.reply(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
     f"Погода у місті: {city}\nТемпература: {cur_temp}°C {wd}\n"
     f"Влажність: {humidity}%\nТиск: {math.ceil(pressure/1.333)} мм.рт.ст\nВітер: {wind} м/с \n"
     f"Схід сонця: {sunrise_timestamp}\nЗахід сонця: {sunset_timestamp}\nТривалість дня: {length_of_the_day}\n"
     f"Хай щастить!"
		)
	except:
	        await message.reply("Перевірте назву міста!")

async def startup(dp: Dispatcher):
	print("started")

if __name__ == "__main__":
	executor.start_polling(dp, on_startup=startup)
