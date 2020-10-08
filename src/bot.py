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

import asyncio
import logging
import requests
import requests_cache
import urllib.request

# TODO: Replace the logging/token mechanism.
# A combination of configparser and environment variables could work.

token = "" # Use your own token here.

logging.basicConfig(
    format="[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
    level=logging.DEBUG
)

bot = telebot.AsyncTeleBot(token=token)

# Main menu

main_button1 = types.KeyboardButton('Download')
main_button2 = types.KeyboardButton('About')

main_markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
main_markup.add(main_button1, main_button2)

# Providers/Settings
## TODO: Move the (volatile) links to a separate file.
## This should be done in order to achieve a higher
## level of consistency with the gettor project, as well
## as because keeping things clean is good.

ia_button = types.KeyboardButton('Internet Archive')
gdrive_button = types.KeyboardButton('Google Drive')

ia_link = "https://archive.org/details/@gettor"
gdrive_link = "https://drive.google.com/open?id=13CADQTsCwrGsIID09YQbNz2DfRMUoxUU"

tor_url = "https://aus1.torproject.org/torbrowser/update_3/release/downloads.json"
source_link = "https://github.com/panos/OnionSproutsBot"

# Download menu
## TODO: Improve the user interface.
source_markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
source_markup = types.ReplyKeyboardMarkup()
source_markup.add(ia_button, gdrive_button)


@bot.message_handler(commands=['help', 'start'])
def welcome(message):
    bot.reply_to(message, 'Welcome! What would you like me to do?', reply_markup=main_markup)


@bot.message_handler(func=lambda msg: msg.text == "Download")
def download_menu(message):
    bot.reply_to(message, 'Where would you like to download Tor from?', reply_markup=source_markup)


@bot.message_handler(func=lambda msg: msg.text == "Internet Archive")
def download_ia(message):
    bot.reply_to(message, f'You can obtain a version of the Tor browser here; {ia_link}', reply_markup=main_markup)


@bot.message_handler(func=lambda msg: msg.text == "Google Drive")
def download_gdrive(message):
    bot.reply_to(message, f'You can obtain a version of the Tor browser here: {gdrive_link}', reply_markup=main_markup)


@bot.message_handler(func=lambda msg: msg.text == "About")
def info(message):
    bot.reply_to(message, f'The source code for this bot can be found here: {source_link}', reply_markup=main_markup)


bot.polling()

