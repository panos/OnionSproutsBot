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

### Design & Documentation

Since the design of the bot hasn't been finalized yet, there's currently no documentation. However, the design and the thought process that have gone into this have been extensively documented.

- [Original thread at The Tor Project's GitLab](https://gitlab.torproject.org/tpo/anti-censorship/gettor-project/trac/-/issues/22011).

In a nutshell, the bot uses the [Pyrogram](https://github.com/pyrogram/pyrogram) library, which is relatively harder to use, but much more powerful. The library takes advantage of Telegram's [MTProto](https://core.telegram.org/mtproto) protocol, rather than the [Bot API](https://core.telegram.org/bots/api), particularly because of a size limit of 50 MBs that could not be bypassed in any way whatsoever.

P.S. Yes, I even tried to message [Pavel Durov](https://en.wikipedia.org/wiki/Pavel_Durov) on LinkedIn to get the restriction lifted and it didn't really work.
