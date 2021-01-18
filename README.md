# OnionSproutsBot

Telegram bot for delivering The Tor Project's software to people in sensitive geographical areas.

## Installing

- Install the required Python modules.

Running `pip3 install -r requirements.txt` should suffice on a system with [Python 3.6+](https://python.org) and [pip](https://pypi.org/project/pip/) installed.

- Follow [Pyrogram's Project Setup Guide](https://docs.pyrogram.org/intro/setup).

You will need a Telegram account, as well as a bot account that can also be created with the help of [BotFather](https://t.me/BotFather)

- After you're done, edit `src/config.py` accordingly.

You need to enter your API key, your application's API hash and your bot's access token. You can also use an access token.

- Head to the `src` directory in a terminal.

If you're on a Unix-like system, you should run `cd src`.

- If a `.session` file is not present, you will be asked to enter a phone number and an access code.

Make sure you're using an interactive terminal when running the bot for the first time. This will generate a file ending in `.session`, which you can also copy to other machines. Make sure to keep your credentials secret!

## Status

The bot is currently under active development and in experimental stages and **should not be used** in production environments.

### Mirrors & Issue Tracking

Currently, the bot is being developed on [The Tor Project's GitLab instance](https://gitlab.torproject.org/tpo/anti-censorship/gettor-project/onionsproutsbot) and is a part of the [gettor project](https://gitlab.torproject.org/tpo/anti-censorship/gettor-project/). There's also a mirror on GitHub, but issues are only being tracked on GitLab, particularly because of a lack of external feedback on the platform.

- [GitLab Repository](https://gitlab.torproject.org/tpo/anti-censorship/gettor-project/onionsproutsbot)
- [GitHub Mirror](https://github.com/panos/OnionSproutsBot)

## Design & Documentation

Since the design of the bot hasn't been finalized yet, there's currently no formal documentation. However, the design and the thought process that have gone into this have been extensively documented, and the current revision of the code always include comments that correspond to the problems that are currently being dealt with. Older revisions may also include additional details.

- [Original thread at The Tor Project's GitLab](https://gitlab.torproject.org/tpo/anti-censorship/gettor-project/trac/-/issues/22011).

### Why Pyrogram?

[Pyrogram](https://pyrogram.org), unlike other libraries, does not interact with [Telegram's Bot API](https://core.telegram.org/bots/api), but uses MTProto instead. MTProto is essentially the library that Telegram clients use.

Using MTProto is fundamental to our cause, because it's bound to the same limitations that an actual user is, despite it being harder to use. A user can upload files that are as large as 2 GBs and initiate secret chats. Bots can normally only upload files up to 50 MBs. 

I also attempted to write the bot using the [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot), which is syntactically similar in many ways. That allowed me to copy and paste most of the code, but I had to rethink a lot of design decisions from scratch.

(P.S. Yes, I even tried to message [Pavel Durov](https://en.wikipedia.org/wiki/Pavel_Durov) on LinkedIn to get the restriction lifted and it didn't really work.)

### Philosophy

It has been brought up to me that others have managed to solve similar problems like the ones that will be solved by this project. 

One of the reasons why development is relatively slow is that I've arguably spent more time doing research and trying out many different implementations through trial and error. I can confidently say that although other implementations may be helpful, **they are very often not the same.**

Here's a list of our goals in order to better describe what differentiates our project from others:

- **This bot should deal with a large sum of users concurrently.**

- **This bot should be easily expandable, sustainable, and easily adaptable.**

If another, new technology arises as a result of the *"Censorship Arms Race"* or if Telegram itself decides to crack down on the distribution of binaries for political reasons, the project has to remain operational.

- **This bot should be useful to people from different cultural and socioeconomic backgrounds.**

That means that the bot has to be accessible, easy to use and available in different languages. Factors, such as low bandwidth, disabilities or the manufacturing date of their mobile phone, should be irrelevant.

- **This bot should be resilient towards abuse and render DDoS attacks meaningless.**

The bot has to waste as few computational resources as possible and respond to queries as fast as possible.

- **This bot has to use a library that's arguably not as widely used as other competing libraries.**

That results in having to explore unexplored territories regularly.

- **This bot must protect the user's privacy as much as possible.**

This means that data arrays or databases that store preferences are prohibitive, while other technologies implemented by the platform, such as [Secret Chats](https://telegram.org/faq#q-how-are-secret-chats-different), have to be further explored and implemented.

- **This bot should be friendly to people starting out with Python.**

Appealing to a large sum of people requires the feedback and the input of some of those people. We should strive to play by the rules, while refraining from using excessively complicated hacks in order to make things work in a way that does not ensure a higher level of efficiency. Many people would be interested in utilizing their knowledge in a way that contributes to their society, while leaving a mark. Therefore, we should make sure that this bot is extensively documented and marketable to audiences that aren't very well versed in Python.
