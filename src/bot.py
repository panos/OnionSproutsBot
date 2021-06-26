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


# TODO: Show a progress bar in a Telegram message instead of using stdout.
def progress(current, total):
    print(f"{current / total * 100:.1f}%")

# TODO: Improve path.
async def relay_files(
    client: Client,
    callback: str,
    url: str,
    original_name: str,
    final_name: str
) -> int:
    data = requests.get(url, allow_redirects=True, stream=True)
    send_success = False

    with open(f'../downloads/{final_name}', 'wb') as f:
        f.write(data.content)

    try:
        file_object = await client.send_document(
            callback.from_user.id,
            document = f"../downloads/{final_name}",
            file_name = original_name,
            progress = progress
        )

        file_id = file_object["document"]["file_id"]
        send_success = True

        # TODO: Remove this, this is a temporary means of testing whether file IDs work properly.
        await client.send_cached_media(callback.from_user.id, file_id=file_id)
    except Exception as e:
        print(e)
        await client.send_message(
            callback.from_user.id,
            f"Upload failed! Reason: `{e}`"
        )

    if send_success == True:
        return file_id
    else:
        return -1


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
            text="Hi, welcome to OnionSproutsBot! What would you like to do?",
	    reply_markup=InlineKeyboardMarkup(
	            [
                        [InlineKeyboardButton("Download The Tor Browser (Desktop)", "request_tor")],
                        [InlineKeyboardButton("What is Tor?", "explain_tor")]
                    ]
            )
        )


@OnionSproutsBot.on_callback_query(filters.regex("explain_tor"))
async def send_explanation(client, callback):
    await client.send_message(callback.from_user.id, "This is a placeholder.")


'''
People generally don't cryptographically verify binaries. It could be a
good idea to take advantage of the nature of an IM platform and teach
people how to do that in a user-centered manner. Splitting this into
a selection prompt where the user consents to being sent a copy of Tor
could be beneficial.
'''

@OnionSproutsBot.on_callback_query(filters.regex("request_tor"))
async def tor_requested(client, callback):
    await client.send_message(callback.from_user.id, "Got it! I will ask you a few questions first.")

    platform_keyboard = []

    for platform in response['downloads'].keys():
        platform_keyboard.append(InlineKeyboardButton(
            text=platform,
            callback_data='select_locale:' + platform
            )
        )

    platform_markup = InlineKeyboardMarkup([platform_keyboard])
    await client.send_message(callback.from_user.id, "Which operating system are you using?", reply_markup=platform_markup)


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
    await client.send_message(callback.from_user.id, "Which language would you like to use?", reply_markup=platform_markup)


@OnionSproutsBot.on_callback_query(filters.regex("download_tor"))
async def send_tor(client, callback):
    # TODO: Remove this print statement.
    print(callback.data)
    platform = callback.data.split(':')[1]
    locale = callback.data.split(':')[2]
    user_id = callback.from_user.id
    send_sig_success = False
    send_bin_success = False
    found_in_database = False

    '''
    Detecting the language that the user speaks is not reliable
    and the codes that Telegram gives us appear as `en`, rather
    than e.g. `en-US`, which is what the endpoint needs. Manual
    conversions are unreliable and bothersome.

    The code used to test this was:
    `locale = callback.from_user.language_code`
    '''

    await client.send_message(user_id, "OK!")

    tor_sig_url = response['downloads'][platform][locale]['sig']
    tor_bin_url = response['downloads'][platform][locale]['binary']

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

    tor_sig_original_name = tor_sig_url.rsplit('/')[-1]
    tor_bin_original_name = tor_bin_url.rsplit('/', 1)[-1]

    # TODO: Check if a copy has already been uploaded to Telegram.

    tor_sig_name = f"{tor_sig_original_name.rsplit('.')[0]}-{time()}.tar.xz.asc"
    tor_bin_name = f"{tor_bin_original_name.rsplit('.')[0]}-{time()}.tar.xz"

    await client.send_message(user_id, "Sending the files right now, please wait...")

    if found_in_database == False:
        tor_sig_id = await relay_files(
            client,
            callback,
            tor_sig_url,
            tor_sig_original_name,
            tor_sig_name
        )

        tor_bin_id = await relay_files(
            client,
            callback,
            tor_bin_url,
            tor_bin_original_name,
            tor_bin_name
        )


    if tor_sig_id != -1:
        send_sig_success == True

    if tor_bin_id != -1:
        send_bin_success == True

    '''
    TODO: Store `tor_sig_file.id and tor_bin_file.id` in a database.
    Handle download and HTTP request failures.
    '''

    # This could be written in a simpler manner with a lambda operator
    # but doing so will overcomplicate the code for no reason and deter
    # maintainers and prospective contributors from ever touching it.
    if send_bin_success == True and send_sig_success == True:
        upload_succeeded = True
    else:
        upload_succeeded = False

    if upload_succeeded == True:
        # TODO: Store tor_bin_id and tor_sig_id in database.
        pass
    elif upload_succeeded == False and found_in_database == True:
        # TODO: Do not do anything.
        pass
    else:
        # TODO: What could possibly go wrong? Should this case be handled earlier on?
        pass


OnionSproutsBot.run()
