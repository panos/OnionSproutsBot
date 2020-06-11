#!/usr/bin/env python
#
# This file is part of OnionSpoutsBot, a Tor Browser distribution Telegram bot.
#
# :authors: Panagiotis Vasilopoulos <hello@alwayslivid.com>
#
# :copyright:   (c) 2020, Panagiotis Vasilopoulos
#
# :license: This is Free Software. See LICENSE for license information.
#

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

# download_markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
# download_markup = types.ReplyKeyboardMarkup()

# TODO: Should these buttons be used for programs, or platforms?
# TODO: Fetch/parse different versions/locales into different buttons.

# download_button1 = types.KeyboardButton('Program 1')
# download_button2 = types.KeyboardButton('Program 2')
# download_button3 = types.KeyboardButton('Program 3')

# download_markup.row(download_button1, download_button2, download_button3)

# TODO: Make the strings translation friendly.


main_markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)

main_button1 = types.KeyboardButton('Download')
main_button2 = types.KeyboardButton('About')

main_markup.row(main_button1, main_button2)


ia_button = types.KeyboardButton('Internet Archive')
gdrive_button = types.KeyboardButton('Google Drive')

source_markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
source_markup = types.ReplyKeyboardMarkup()
source_markup.row(ia_button, gdrive_button)

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, 'Welcome! What would you like me to do today?', reply_markup=main_markup)


@bot.message_handler(func=lambda msg: msg.text == "Download")
def download(message):
    bot.reply_to(message, 'Where would you like to download Tor from?', reply_markup=source_markup)

@bot.message_handler(func=lambda msg: msg.text == "Internet Archive")
def download(message):
    bot.reply_to(message, 'You can obtain a version of the Tor browser here; https://archive.org/details/@gettor', reply_markup=main_markup)

@bot.message_handler(func=lambda msg: msg.text == "Placeholder")
def download(message):
    bot.reply_to(message, 'You can obtain a version of the Tor browser here; https://example.com', reply_markup=main_markup)


@bot.message_handler(func=lambda msg: msg.text == "About")
def info(message):
    bot.reply_to(message, 'The source code for this bot can be found here; https://github.com/AlwaysLivid/OnionSproutsBot')

bot.polling()
