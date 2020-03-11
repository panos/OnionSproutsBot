#!/usr/bin/env python
#
# Copyright (C) 2020
# Panagiotis Vasilopoulos <hello@alwayslivid.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser Public License for more details.
#
# You should have received a copy of the GNU Lesser Public License
# along with this program.  If not, see [http://www.gnu.org/licenses/].

import telebot
from telebot import types

import logging


# TODO: Replace the logging/token mechanism.

token = "" # Use your own token here.

logging.basicConfig(
    format="[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
    level=logging.DEBUG
)

bot = telebot.AsyncTeleBot(token=token)

# TODO: Language submenu with additional options.
# Maybe using country flags would be a solid idea, considering that language barriers
# would not get in the way.
#
# one_time_keyboard instantly closes the keyboard. It works flawlessly, but
# maybe using types.RemoveKeyboardMarkup() after sending the message in the next function
# and then replacing it could be a better idea that'd make the bot more user friendly.
#

main_markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)

main_button1 = types.KeyboardButton('📥')
main_button2 = types.KeyboardButton('ℹ️')

main_markup.row(main_button1, main_button2)



download_markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)

download_markup = types.ReplyKeyboardMarkup()

# TODO: Should these buttons be used for programs, or platforms?

download_button1 = types.KeyboardButton('Program 1')
download_button2 = types.KeyboardButton('Program 2')
download_button3 = types.KeyboardButton('Program 3')

download_markup.row(download_button1, download_button2, download_button3)


# TODO: Make the strings translation friendly.

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, 'Welcome! What would you like me to do today?', reply_markup=main_markup)

@bot.message_handler(func=lambda msg: msg.text == "📥")
def welcome(message):
    bot.reply_to(message, 'What would you like to download?', reply_markup=download_markup)


@bot.message_handler(func=lambda msg: msg.text == "ℹ️")
def welcome(message):
    bot.reply_to(message, 'Developed by AlwaysLivid.')

bot.polling()
