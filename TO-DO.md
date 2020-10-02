# TO-DO

This file contains a set of desired tasks that should be considered.

Please note that the [bot's source code](src/bot.py) contains a lot of additional notes that are more specific and represent design-related issues and thoughts at the time of authoring.

## Tasks

- Make strings translation-friendly.

- Add a language submenu to the Telegram bot, in order to allow people to easily switch between locales. Fetch the corresponding locale of the Tor browser, after asking the user whether using the currently selected locale is okay. If not, allow them to select the locale by themselves.

- Create buttons dynamically depending on the available operating systems and versions.

- Use classes and organize the code accordingly, so that it will be easier to integrate it to gettor later on, without too many structural changes.

- Imitate the way gettor does logging.

- Give the bot the ability to act as a means of distribution (alongside Google Drive and the Internet Archive), for the sake of convenience and in order to accomodate users that are in jurisdictions where both websites are blocked (either temporarily or permanently). This will be particularly more useful in the former situation, considering that Telegram, as a platform, has historically persisted under sudden, specific measures of censorship.

- It would be a good idea to think about whether Telegram (as well as the bot) could also work as an informative resource.

- Improve the way credentials are stored, used and handled.

- (Maybe?) Give the bot the ability to provide the user with bridges (with protection layers similar to the ones in The Tor Browser itself, such as CAPTCHAs).
