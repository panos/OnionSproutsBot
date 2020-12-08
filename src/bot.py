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
                            InlineKeyboardMarkup, InlineKeyboardButton)


class User:
    def __init__(self, platform, locale):
        self.locale = platform
        self.platform = locale


global response
response = requests.get(endpoint).json()

OnionSproutsBot = Client(
    "OnionSproutsBot",
    apiId,
    apiHash,
    bot_token=botToken
)

# TO-DO: Remove this and replace it with callbacks.
user = User(
   locale = "en-US",
   platform = "win64"
)


@OnionSproutsBot.on_message(filters.command("start"))
async def start_command(client, message):
        await client.send_message(
            chat_id=message.chat.id,
            text="Hi, welcome to OnionSproutsBot! Press the button if you wish to receive a copy of The Tor Browser.",
	    reply_markup=InlineKeyboardMarkup(
	            [
                        [InlineKeyboardButton("Receive a copy of Tor", "send_tor")],
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

@OnionSproutsBot.on_callback_query(filters.regex("send_tor"))
async def send_binary(client, callback):
    print("User clicked on the button.")
    await client.send_message(callback.from_user.id, "Got it! I'm going to download then send you the program, as well as a cryptographic signature, in order for you to be able to establish that this copy of The Tor Browser is legitimate. Please wait for a while...")

    tor_sig = response['downloads'][user.locale][user.platform]['sig']
    tor_binary = response['downloads'][user.locale][user.platform]['binary']

    download_sig = requests.get(tor_sig, allow_redirects=True, stream=True)
    download_binary = requests.get(tor_binary, allow_redirects=True, stream=True)

    with open('../downloads/tor_sig.tar.xz', 'wb') as f:
        f.write(download_sig.content)

    with open('../downloads/tor.tar.xz', 'wb') as f:
        f.write(download_binary.content)

    await client.send_document(callback.from_user.id, document="../downloads/tor_sig.tar.xz")
    await client.send_document(callback.from_user.id, document="../downloads/tor.tar.xz")


OnionSproutsBot.run()
