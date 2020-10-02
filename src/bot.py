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

main_markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
main_button1 = types.KeyboardButton('Download')
main_button2 = types.KeyboardButton('About')

main_markup.row(main_button1, main_button2)

# Providers/Settings
## TODO: Move the (volatile) links to a separate file.
## This should be done in order to achieve a higher
## level of consistency with the gettor project, as well
## as because keeping things clean is good.


ia_button = types.KeyboardButton('Internet Archive')
gdrive_button = types.KeyboardButton('Google Drive')
telegram_button = types.KeyboardButton('Telegram')

ia_link = "https://archive.org/details/@gettor"
gdrive_link = "https://drive.google.com/open?id=13CADQTsCwrGsIID09YQbNz2DfRMUoxUU"

tor_url = "https://aus1.torproject.org/torbrowser/update_3/release/downloads.json"
source_link = "https://github.com/panos/OnionSproutsBot"

# Download menu
## TODO: Improve the user interface.
source_markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
source_markup = types.ReplyKeyboardMarkup()
source_markup.row(ia_button, gdrive_button, telegram_button)

user_dict = {}


# When using bot.register_next_step_handler, parsing variables other than
# the message itself is not currently possible. Therefore, creating an
# instance of a class representing the user is more viable.

class User:
    def __init__(self, platform):
        self.platform = platform
        self.locale = None


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


@bot.message_handler(func=lambda msg: msg.text == "Telegram")
def download_telegram(message):
    global response
    response = requests.get(tor_url).json()

    platform_markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    platform_markup = types.ReplyKeyboardMarkup()

    for key in response['downloads'].keys():
        platform_markup.add(types.InlineKeyboardButton(text=key))

    bot.reply_to(message, 'Which platform do you wish to run The Tor Browser on?', reply_markup=platform_markup)
    bot.register_next_step_handler(message, select_platform)


# TODO: Handle unexpected input.
#
# Making sure that it works in the first place is more important to me
# than ensuring it works in every case.
def select_platform(message):
    chat_id = message.chat.id
    platform = message.text
    user = User(platform)
    user_dict[chat_id] = user

    locale_markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    locale_markup = types.ReplyKeyboardMarkup()

    print(response['downloads'])
    print(message.text)

    print(user.platform)

    for key in response['downloads'][user.platform]:
        locale_markup.add(types.InlineKeyboardButton(text=key))

    bot.reply_to(message, 'What is your desired locale?', reply_markup=locale_markup)
    bot.register_next_step_handler(message, send_download)


# TODO: Sending a Tor archive is not possible over Telegram, because Telegram
# has implemented a 50 MB limit that only applies to bots. I'd like to reach
# out to Telegram to examine whether an exception can be made (due to aligning
# values), but I haven't been able to succeed in doing so.
#
# If Telegram (which is quite resistant to censorship efforts) is to be used
# as a mirror, any archives over 50 megabytes have to be stored locally
# and split. However, that would require providing the user with sufficient,
# clear details on how to put the split archives back together and I'm also
# not sure if verifying the archive is still going to be possible after the
# processing.
#
# I had already imagined that making a bot that would appeal to users with
# limited technological skills would require bundling together some
# documentation (after all, the supposed user does not have access to anything
# else other than Telegram), but this increases the level of complexity.
#
# I am not sure whether the library in use will manage to handle sending data
# when in use by mass amounts of people concurrently. The developers of
# pyTelegramAPI advertise their library as asynchronous.
#
# P.S. The opinionated naming of the archives is there for testing.
def send_download(message):
    chat_id = message.chat.id
    locale = message.text
    user = user_dict[chat_id]

    tor_binary = response['downloads'][user.platform][locale]['binary']
    tor_sig = response['downloads'][user.platform][locale]['sig']

    download_binary = requests.get(tor_binary, allow_redirects=True, stream=True)
    download_sig = requests.get(tor_sig, allow_redirects=True, stream=True)

    with open('tor.tar.xz', 'wb') as f:
        f.write(download_binary.content)

    with open('tor_sig.tar.xz', 'wb') as f:
        f.write(download_sig.content)

    bot.reply_to(message, tor_binary)
    bot.reply_to(message, tor_sig)

    binary = open('tor.tar.xz', 'rb')
    sig = open('tor_sig.tar.xz', 'rb')
    test = bot.send_document(chat_id, binary)
    bot.send_document(chat_id, sig)

    print(test)

    bot.reply_to(message, "Here you go!")


def select_locale(message):
    response = requests.get(tor_url).json()
    exit()


@bot.message_handler(func=lambda msg: msg.text == "About")
def info(message):
    bot.reply_to(message, f'The source code for this bot can be found here: {source_link}', reply_markup=main_markup)


bot.polling()

