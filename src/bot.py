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

from config import *

import asyncio
import requests
import re
from requests import HTTPError

from pyrogram import Client, filters
from pyrogram.types import (InlineQueryResultArticle, InputTextMessageContent,
                            InlineKeyboardMarkup, InlineKeyboardButton,
                            KeyboardButton, ReplyKeyboardMarkup)


global response
response = requests.get(endpoint).json()

OnionSproutsBot = Client(
    "OnionSproutsBot",
    apiId,
    apiHash,
    bot_token=botToken
)


@OnionSproutsBot.on_message(filters.command("start"))
async def start_command(client, message):
        await client.send_message(
            chat_id=message.chat.id,
            text="Hi, welcome to OnionSproutsBot! Press the button if you wish to receive a copy of The Tor Browser.",
	    reply_markup=InlineKeyboardMarkup(
	            [
                        [InlineKeyboardButton("Receive a copy of Tor", "request_tor")],
                        [InlineKeyboardButton("What is Tor?", "explain_tor")]
                    ]
            )
        )


# This is currently an interesting way of testing asynchronous operations.
# Works on my machine!
@OnionSproutsBot.on_callback_query(filters.regex("explain_tor"))
async def send_explanation(client, callback):
    await client.send_message(callback.from_user.id, "That's a good question!")
    await asyncio.sleep(2)
    await client.send_message(callback.from_user.id, "... Hm... Uh...")
    await asyncio.sleep(4)
    await client.send_message(callback.from_user.id, "... Well, that's awkward. I'll probably give you an answer once I organize the strings a bit better.")


@OnionSproutsBot.on_callback_query(filters.regex("request_tor"))
async def tor_requested(client, callback):
    await client.send_message(callback.from_user.id, "Got it! I'm going to download then send you the program, as well as a cryptographic signature, in order for you to be able to establish that this copy of The Tor Browser is legitimate.")
    platform_keyboard = []

    for platform in response['downloads'].keys():
        platform_keyboard.append(InlineKeyboardButton(
            text=platform,
            callback_data='select_locale:' + platform
            )
        )

    platform_markup = InlineKeyboardMarkup([platform_keyboard])
    await client.send_message(callback.from_user.id, "Please select your platform:", reply_markup=platform_markup)


# TO-DO: Ask for the locale when the user initiates the bot, rather
# than afterwards, and change the language the bot speaks automatically.
#
# How do we know what locales are available, and how do we know
# that the locale for one program is going to be available for another?
@OnionSproutsBot.on_callback_query(filters.regex("select_locale:"))
async def tor_requested(client, callback):
    platform_keyboard = []
    platform = callback.data.split(':')[1]

    for locale in response['downloads'][platform].keys():
        platform_keyboard.append(InlineKeyboardButton(
            text=locale,
            callback_data='download_tor:' + platform + ':' + locale
            )
        )

    platform_markup = InlineKeyboardMarkup([platform_keyboard])
    await client.send_message(callback.from_user.id, "Now, select your locale:", reply_markup=platform_markup)


@OnionSproutsBot.on_callback_query(filters.regex("download_tor"))
async def send_tor(client, callback):
    print(callback.data)
    platform = callback.data.split(':')[1]
    locale = callback.data.split(':')[2]
    # locale = callback.from_user.language_code
    # Detecting the language that the user speaks is not reliable
    # and the codes that Telegram gives us appear as `en`, rather
    # than e.g. `en-US`, which is what the endpoint needs.

    await client.send_message(callback.from_user.id, "Sounds good! I'm going to send you the files now, please wait...")

    # TO-DO: Upload Tor binaries/signatures on a channel automatically.
    # We could wait upload every single version in every single locale
    # and then store the cache_id's in order to forward the binaries
    # immediately, but that would result in tons of wasted bandwidth
    # and I worry about the bot not being able to keep up.
    # Therefore, it's better to provide people with what they need.
    tor_sig = response['downloads'][platform][locale]['sig']
    tor_binary = response['downloads'][platform][locale]['binary']

    # Is using allow_redirects secure?
    download_sig = requests.get(tor_sig, allow_redirects=True, stream=True)
    download_binary = requests.get(tor_binary, allow_redirects=True, stream=True)

    # TO-DO: Write files asynchronously.
    # TO-DO: Use the file names of the actual files themselves.
    with open('../downloads/tor_sig.tar.xz', 'wb') as f:
        f.write(download_sig.content)

    with open('../downloads/tor.tar.xz', 'wb') as f:
        f.write(download_binary.content)

    await client.send_document(callback.from_user.id, document="../downloads/tor_sig.tar.xz")
    await client.send_document(callback.from_user.id, document="../downloads/tor.tar.xz")


OnionSproutsBot.run()
