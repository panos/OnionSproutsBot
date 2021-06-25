#!/usr/bin/env python3
#
# This file is part of OnionSpoutsBot, a Tor Browser distribution Telegram bot.
#
# :authors: Panagiotis Vasilopoulos <hello@alwayslivid.com>
#
# :copyright:   (c) 2020-2021, Panagiotis Vasilopoulos
#
# :license: This is Free Software. See LICENSE for license information.
#

from config import *

import asyncio
import io
import os
import requests
import re
from requests import HTTPError
import urllib

from time import time
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

def progress(current, total):
    print(f"{current / total * 100:.1f}%")


'''
TO-DO: Ask for the locale when the user initiates the bot, rather
than afterwards, and change the language the bot speaks automatically.

The language should be asked for initially before showing this selection screen.
That way, the instructions and all relevant documentation will be readable and completely
understood by the user. For that reason, the bot needs to cache a list of available (or all)
locales in the future.
'''


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


@OnionSproutsBot.on_callback_query(filters.regex("explain_tor"))
async def send_explanation(client, callback):
    await client.send_message(callback.from_user.id, "This is a placeholder.")


@OnionSproutsBot.on_callback_query(filters.regex("request_tor"))
async def tor_requested(client, callback):
    await client.send_message(callback.from_user.id, "Got it! I'm going to download, then send you, a copy of The Tor Browser.")

    '''
    People generally don't cryptographically verify binaries. It could be a
    good idea to take advantage of the nature of an IM platform and teach
    people how to do that in a user-centered manner. Splitting this into
    a selection prompt where the user consents to being sent a copy of Tor
    could be beneficial.
    '''

    await client.send_message(callback.from_user.id, "I will also send you a cryptographic signature, in order for you to be able to establish that it is legitimate.")

    platform_keyboard = []

    for platform in response['downloads'].keys():
        platform_keyboard.append(InlineKeyboardButton(
            text=platform,
            callback_data='select_locale:' + platform
            )
        )

    platform_markup = InlineKeyboardMarkup([platform_keyboard])
    await client.send_message(callback.from_user.id, "Please select your platform:", reply_markup=platform_markup)


@OnionSproutsBot.on_callback_query(filters.regex("select_locale:"))
async def locale_selected(client, callback):
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

    '''
    Detecting the language that the user speaks is not reliable
    and the codes that Telegram gives us appear as `en`, rather
    than e.g. `en-US`, which is what the endpoint needs. Manual
    conversions are unreliable and bothersome.

    The code used to test this was:
    `locale = callback.from_user.language_code`
    '''

    await client.send_message(callback.from_user.id, "OK!")

    tor_sig = response['downloads'][platform][locale]['sig']
    tor_bin = response['downloads'][platform][locale]['binary']

    send_sig_success = False
    send_bin_success = False

    '''
    Each of the two files have an original name, as described by the
    tor_sig_original_name and tor_bin_original_name variables, which
    store the original file name of the Tor Browser. An example of
    such a name would be "tor-browser-linux32-10.0.12_en-US.tar.xz".

    However, we cannot store the files with their original names as-is,
    due to a couple of edge cases, such as when two users request for
    the same file at the same time. For that reason, I found that it
    would be a good idea to create a new name that consists of a
    new name generated by the original name and the Unix Epoch time.

    That way, conflicts, and therefore, undefined behavior, is
    extremely unlikely to happen. Diagnosing issues should also be easier.
    '''

    tor_sig_original_name = tor_sig.rsplit('/')[-1]
    tor_bin_original_name = tor_bin.rsplit('/', 1)[-1]

    tor_sig_name = f"{tor_sig_original_name.rsplit('.')[0]}-{time()}.tar.xz.asc"
    tor_bin_name = f"{tor_bin_original_name.rsplit('.')[0]}-{time()}.tar.xz"

    await client.send_message(callback.from_user.id, "Sending the files right now, please wait...")

    # Upload the signature.
    download_sig = requests.get(tor_sig, allow_redirects=True, stream=True)

    with open(f'../downloads/{tor_sig_name}', 'wb') as f:
        f.write(download_sig.content)

    try:
        tor_sig_object = await client.send_document(
            callback.from_user.id,
            document = f"../downloads/{tor_sig_name}",
            file_name = tor_sig_original_name,
            progress = progress
        )

        tor_sig_id = tor_sig_object["document"]["file_id"]
        send_sig_success = True

        # TODO: Remove this, this is a temporary means of testing whether file IDs work properly.
        await client.send_cached_media(callback.from_user.id, file_id=tor_sig_id)
    except Exception as e:
        print(e)
        await client.send_message(
            callback.from_user.id,
            f"Signature upload failed! Reason: `{e}`"
        )

    # Upload the binary.
    download_bin = requests.get(tor_bin, allow_redirects=True, stream=True)

    with open(f'../downloads/{tor_bin_name}', 'wb') as f:
        f.write(download_bin.content)

    try:
        tor_bin_object = await client.send_document(
            callback.from_user.id,
            document = f"../downloads/{tor_bin_name}",
            file_name = tor_bin_original_name,
            progress = progress
        )

        tor_bin_id = tor_bin_object["document"]["file_id"]
        send_bin_success = True

        # TODO: Remove this, this is a temporary means of testing whether file IDs work properly.
        await client.send_cached_media(callback.from_user.id, file_id=tor_bin_id)
    except Exception as e:
        print(e)
        await client.send_message(
            callback.from_user.id,
            f"Binary upload failed! Reason: `{e}`"
        )

    '''
    TODO: Store `tor_sig_file.id and tor_bin_file.id` in a database.
    Handle download and HTTP request failures.
    '''

    if send_bin_success == True and send_sig_success == True:
        pass


OnionSproutsBot.run()
