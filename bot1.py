#python bot1.py
import telebot
import random
import requests
import time
import pygame

from random import choice
from bs4 import BeautifulSoup
from telebot import types
from mg import get_map_cell


TOKEN = '2146664030:AAGvSTgfka3qemt09TDLnqi8Wfxcyx3POQo'
bot = telebot.TeleBot(TOKEN)

cols, rows = 8, 8






#Старт
@bot.message_handler(commands = ['start'])
def start(message):
	bot.send_message(message.chat.id, "Привет, юзер! Выбери из списка то, что тебе нужно \n\n\n    Чтобы узнать свой ID или НИК - комманда /info \n    Чтобы узнать новости - комманда /news")




@bot.message_handler(commands = ['news'])
def handle(message):
	URL = 'https://ria.ru/world/'
	HEADERS = {
		'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36'
	}

	response = requests.get(URL, headers = HEADERS)
	soup = BeautifulSoup(response.content, 'html.parser')
	texts = soup.findAll('a', 'list-item__title')

	for i in range(len(texts[:-5]), -1, -1):
		txt = str(i + 1) + ') ' + texts[i].text
		bot.send_message(message.chat.id, '<a href="{}">{}</a>'.format(texts[i]['href'], txt), parse_mode = 'html')



@bot.message_handler(commands=['info'])
def get_info(message):
	markup_inline = types.InlineKeyboardMarkup()
	item_yes = types.InlineKeyboardButton(text = 'Да', callback_data = 'yes')
	item_no = types.InlineKeyboardButton(text = 'Нет', callback_data = 'no')

	markup_inline.add(item_yes, item_no)
	bot.send_message(message.chat.id, "Желаете узнать ваш ник и ID?",
		reply_markup = markup_inline
		)


@bot.callback_query_handler(func = lambda call: True)
def answer(call):
	if call.data == 'yes':
		markup_reply = types.InlineKeyboardMarkup()
		item_id = types.InlineKeyboardButton(text ='Мой ID', callback_data = 'id')
		item_username = types.InlineKeyboardButton(text = 'Мой ник', callback_data = 'nick')
		markup_reply.add(item_id, item_username)
		bot.send_message(call.message.chat.id,'Нажмите на одну из кнопок',
			reply_markup = markup_reply
			)	

@bot.callback_query_handler(func = lambda call: True)
def answer(call):
	if call.data == 'id':
		bot.send_message(message.chat.id, f'Your ID: {message.from_user.id}')

	elif call.data == 'nick':
		bot.send_message(message.chat.id, f'Your name: {message.from_user.first_name} {message.from_user.last_name}');

	
	elif call.data == 'no':
		pass


	
		
#labirint
from mg import get_map_cell





cols, rows = 8, 8

keyboard = telebot.types.InlineKeyboardMarkup()
keyboard.row( telebot.types.InlineKeyboardButton('←', callback_data='left'),
			  telebot.types.InlineKeyboardButton('↑', callback_data='up'),
			  telebot.types.InlineKeyboardButton('↓', callback_data='down'),
			  telebot.types.InlineKeyboardButton('→', callback_data='right') )

maps = {}

def get_map_str(map_cell, player):
	map_str = ""
	for y in range(rows * 2 - 1):
		for x in range(cols * 2 - 1):
			if map_cell[x + y * (cols * 2 - 1)]:
				map_str += "⬛"
			elif (x, y) == player:
				map_str += "🔴"
			else:
				map_str += "⬜"
		map_str += "\n"

	return map_str

@bot.message_handler(commands=['play'])
def play_message(message):
	map_cell = get_map_cell(cols, rows)

	user_data = {
		'map': map_cell,
		'x': 0,
		'y': 0
	}

	maps[message.chat.id] = user_data

	bot.send_message(message.from_user.id, get_map_str(map_cell, (0, 0)), reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_func(query):
	user_data = maps[query.message.chat.id]
	new_x, new_y = user_data['x'], user_data['y']

	if query.data == 'left':
		new_x -= 1
	if query.data == 'right':
		new_x += 1
	if query.data == 'up':
		new_y -= 1
	if query.data == 'down':
		new_y += 1

	if new_x < 0 or new_x > 2 * cols - 2 or new_y < 0 or new_y > rows * 2 - 2:
		return None
	if user_data['map'][new_x + new_y * (cols * 2 - 1)]:
		return None

	user_data['x'], user_data['y'] = new_x, new_y

	if new_x == cols * 2 - 2 and new_y == rows * 2 - 2:
		bot.edit_message_text( chat_id=query.message.chat.id,
							   message_id=query.message.id,
							   text="Вы выиграли" )
		return None

	bot.edit_message_text( chat_id=query.message.chat.id,
						   message_id=query.message.id,
						   text=get_map_str(user_data['map'], (new_x, new_y)),
						   reply_markup=keyboard )












    














bot.polling(none_stop = True, interval = 0)
