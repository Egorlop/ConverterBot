import telebot
from bs4 import BeautifulSoup
import requests
from telebot import types
import datetime
converter = telebot.TeleBot('1401850820:AAFIlzqtJn20Me0O74aqJ9_0wf-tGHsPmRc')

def isfloat(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
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
	final_message=" "
	today = str(datetime.datetime.now())
	messagelow = message.text.strip().lower()
	courses = parse()
	buttons = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
	if messagelow == "курсы валют на сегодня":
		button1 = types.KeyboardButton('USD')
		button2 = types.KeyboardButton('EUR')
		button3 = types.KeyboardButton('GBP')
		button4 = types.KeyboardButton('В меню')
		buttons.add(button1,button2, button3, button4)
		final_message = "Выбери интересующую тебя валюту\n"
	elif messagelow == "конвертер валют":
		final_message = "Введи интересующую тебя сумму и валюту для конвертации в рубли.\nНапример: 49.5$"
	elif messagelow == "usd":
		final_message = f"Курс доллара по отношению к рублю на <b>{today[0:10]}</b> по данным ЦБ РФ:\n1<b> USD</b> = {courses['dollar']}<b> RUB</b>"
	elif messagelow == "eur":
		final_message = f"Курс евро по отношению к рублю на <b>{today[0:10]}</b> по данным ЦБ РФ:\n1<b> EUR </b>= {courses['euro']}<b> RUB</b>"
	elif messagelow == "gbp":
		final_message = f"Курс фунта стерлингов по отношению к рублю на <b>{today[0:10]}</b> по данным ЦБ РФ:\n1<b> GBP</b> = {courses['pound']} <b>RUB</b>"
	elif messagelow=="в меню":
		buttons = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
		button1 = types.KeyboardButton('Курсы валют на сегодня')
		button2 = types.KeyboardButton('Конвертер валют')
		buttons.add(button1, button2)
		final_message = "Выбери дальнейшее действие"
	elif isfloat(messagelow[0:len(messagelow)-1]):
		if messagelow[len(messagelow)-1]=="$":
			final_message = f"По сегодняшнему курсу валют ЦБ РФ имеем:\n{messagelow[0:len(messagelow)-1]} <b>USD</b> = {round(float(messagelow[0:len(messagelow)-1])*float(courses['dollar']),3)} <b>RUB</b>\n"
		if messagelow[len(messagelow)-1]=="€":
			final_message = f"По сегодняшнему курсу валют ЦБ РФ имеем:\n{messagelow[0:len(messagelow)-1]} <b>EUR</b> = {round(float(messagelow[0:len(messagelow)-1])*float(courses['euro']),3)} <b>RUB</b>\n"
		if messagelow[len(messagelow)-1]=="£":
			final_message = f"По сегодняшнему курсу валют ЦБ РФ имеем:\n{messagelow[0:len(messagelow)-1]} <b>GBP</b> = {round(float(messagelow[0:len(messagelow)-1])*float(courses['pound']),3)} <b>RUB</b>\n"
	else:
		final_message = "Неверная команда или формат числа для конвертации"
	converter.send_message(message.chat.id, final_message, parse_mode='html',reply_markup=buttons)

converter.polling(none_stop=True)
