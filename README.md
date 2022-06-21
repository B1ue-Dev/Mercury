# Mercury [![wakatime](https://wakatime.com/badge/github/Jimmy-Blue/Mercury.svg)](https://wakatime.com/badge/github/Jimmy-Blue/Mercury)

![image](https://user-images.githubusercontent.com/60958064/168848928-c9b81d41-e297-4ae9-9748-4f2237f86d2d.png)

Mercury is a simple modmail Discord bot that you can use it in your own server.

# Usage

- Clone this repository.
- Install all packages dependency: ``pip install -r requirements.txt``.
- Put your bot token, guild ID and channel ID you want to use as the modmail channel in the ``.env.example`` file and remove the ``.example``.
- Run the bot: ``python ./src/bot.py``.

# Feature

- A simple moderation mail system that members can use to get in touch with the moderation team.
- Being able to block/unblock members from the bot.

# Guide
- For members: Send a message to the bot in DM. It will send the content to the modmail channel.
- For moderators: Reply to the bot sent message to have your message sent back to the user through the bot.

# Note

- This bot can only be used in a server. It is better to host it by your own and use it in your server.

# Todo

- [ ] Move to SQL instead of json, preferably [SQLite](https://github.com/python/cpython/blob/main/Doc/library/sqlite3.rst).


