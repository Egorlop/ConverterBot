import telebot
from bs4 import BeautifulSoup
import requests
from telebot import types
import datetime
converter = telebot.TeleBot('1401850820:AAGyfTFNi4RL8bxlhxC-qAYUu9lJu7mgN2M')

def convert(str1):
	str= str1
	for i in range(len(str)):
		if str[i] == "$":
			dollar = str[0:i]
			flagdollar = i
		if str[i] == "€":
			euro = str[flagdollar + 2:i]
			flageuro = i
		if str[i] == "£":
			pound = str[flageuro + 2:i]
	convertvalues = {
		'dollar': dollar,
		'euro': euro,
		'pound': pound

	}
	return convertvalues
def parse():
	URL = 'https://finance.rambler.ru/currencies/'
	HEADERS = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.185 YaBrowser/20.11.2.78 Yowser/2.5 Safari/537.36'
	}
	response = requests.get(URL, headers=HEADERS)
	soup = BeautifulSoup(response.content, 'html.parser')
	convert = soup.findAll('div', {'class': 'finance-currency-table__cell finance-currency-table__cell--value'})
	euro = convert[11].text
	pound = convert[12].text
	dollar = convert[29].text
	courses = {
		'dollar': dollar[1:-1],
		'euro': euro[1:-1],
		'pound': pound[1:-1]
	}
	return courses
@converter.message_handler(commands=['start'])
def start(message):
	buttons = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
	button1 = types.KeyboardButton('Курсы валют на сегодня')
	button2 = types.KeyboardButton('Конвертер валют')
	buttons.add(button1, button2)
	start_message = f"<b>Приветствую тебя, {message.from_user.first_name}!</b>\n\n" \
					f"Меня зовут <b>Арчи</b>, и сегодня я стану твоим спутником по миру финансов!\n\n" \
					f"У меня ты всегда можешь узнать текущий курс валют, а так же сконвертировать сразу несколько валют в рубли.\n\n"\
					f"Больше тебе не нужно брать в руки калькулятор и лезть в Гугл в поисках актуальных котировок, ведь всё это есть у меня!\n\nОбращайся в любое время дня и ночи!"
	converter.send_message(message.chat.id, start_message, parse_mode='html', reply_markup=buttons)

@converter.message_handler(content_types=['text'])
def menu(message):
	trigger = 0
	today = str(datetime.datetime.now())
	messagelow = message.text.strip().lower()
	courses = parse()
	buttons = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
	for i in range(len(messagelow)):
		if messagelow[i]=="$" or messagelow[i]=="€" or messagelow[i]=="£" or messagelow[i]==" ":
			trigger+=1
	if messagelow == "курсы валют на сегодня":
		button1 = types.KeyboardButton('$')
		button2 = types.KeyboardButton('€')
		button3 = types.KeyboardButton('£')
		button4 = types.KeyboardButton('В меню')
		buttons.add(button1,button2, button3, button4)
		final_message = "Выбери интересующую тебя валюту\n"
	elif messagelow == "конвертер валют":
		final_message = "<b>Введи набор интересующих тебя валют для конвертации.</b>\n\n" \
						"Обрати внимание, что валюты должны быть введены в строго определенном порядке, без точек и запятых!\n"\
						"<b>Например:</b> '45$ 148€ 15£'"
	elif messagelow == "конвертер валют":
		final_message = "Введи набор интересующих тебя валют для конвертации: "
	elif messagelow == "$":
		final_message = f"Курс доллара по отношению к рублю на <b>{today[0:10]}</b> по данным ЦБ РФ:\n1<b> USD</b> = {courses['dollar']}<b> RUB</b>"
	elif messagelow == "€":
		final_message = f"Курс евро по отношению к рублю на <b>{today[0:10]}</b> по данным ЦБ РФ:\n1<b> EUR </b>= {courses['euro']}<b> RUB</b>"
	elif messagelow == "£":
		final_message = f"Курс фунта стерлингов по отношению к рублю на <b>{today[0:10]}</b> по данным ЦБ РФ:\n1<b> GBP</b> = {courses['pound']} <b>RUB</b>"
	elif messagelow=="в меню":
		buttons = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
		button1 = types.KeyboardButton('Курсы валют на сегодня')
		button2 = types.KeyboardButton('Конвертер валют')
		buttons.add(button1, button2)
		final_message = "Выбери дальнейшее действие"
	elif trigger == 5:
		values=convert(messagelow)
		final_message = f"По сегодняшнему курсу валют ЦБ РФ имеем:\n{values['dollar']} <b>USD</b> = {round(int(values['dollar'])*float(courses['dollar']),3)} <b>RUB</b>\n" \
						f"{values['euro']} <b>EUR</b> = {round(int(values['euro']) * float(courses['euro']),3)} <b>RUB</b>\n" \
						f"{values['pound']} <b>GBP</b> = {round(int(values['pound']) * float(courses['pound']), 3)} <b>RUB</b>\n"
	elif trigger==0:
		final_message = "Выбери дальнейшее действие"
	else:
		final_message="Введи в нужном формате\n<b>Например:</b> '45$ 148€ 15£'"


	converter.send_message(message.chat.id, final_message, parse_mode='html',reply_markup=buttons)

converter.polling(none_stop=True)