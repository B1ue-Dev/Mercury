"""
Modmail system handler.

(C) 2022 - Jimmy-Blue
"""

import re
import io
import json
import datetime
from interactions import (
    extension_listener,
    extension_component,
    Extension,
    Client,
    ComponentContext,
    Message,
    Channel,
    ChannelType,
    File,
    Member,
)
import aiohttp


def _last_index(_list: list) -> any:
    """
    Return the result of the last index in a list.

    :param _list: The list.
    :param type: list
    :return: The result of the last index of the list.
    :rtype: any
    """

    res = int(len(_list)) - 1
    return _list[res]


class Modmail(Extension):
    """Extension handling `MESSAGE_CREATE` gateway event."""

    def __init__(self, client: Client) -> None:
        self.client: Client = client

    @extension_listener(name="on_message_create")
    async def _message_create(self, message: Message):
        channel = await message.get_channel()

        if channel.type == ChannelType.DM:
            if int(message.author.id) == int(self.client.me.id):
                return

            _blocked = json.loads(open("./db/blocked.json", "r").read())

            if str(message.author.id) in _blocked:
                return

            _opened = json.loads(open("./db/opened.json", "r").read())

            if str(message.author.id) not in _opened:
                return await channel.send("You do not have any session opened. Use `/create` to open a new session.")

            thread_id = _opened[str(message.author.id)]["thread_id"]

            _thread = Channel(
                **await self.client._http.get_channel(int(thread_id)),
                _client=self.client._http,
            )

            await _thread.send(
                content="".join(
                    [
                        f"From {message.author.mention}:\n",
                        f"{message.content}",
                    ]
                ),
                files=[File(filename=a.filename, fp=io.BytesIO(await (await aiohttp.ClientSession().get(a.url)).content.read())) for a in message.attachments],
            )

        elif channel.type == ChannelType.GUILD_PUBLIC_THREAD:

            if int(message.author.id) == int(self.client.me.id):
                pass
            else:
                result = re.findall('[0-9]+', str(channel.name))
                user_id = _last_index(result)

                _opened = json.loads(open("./db/opened.json", "r").read())

                if str(channel.id) != _opened[str(user_id)]["thread_id"]:
                    return

                _member = Member(
                    **await self.client._http.get_member(int(message.guild_id), int(user_id)),
                    _client=self.client._http,
                )

                await _member.send(
                    content=f"{message.content}",
                    files=[File(filename=a.filename, fp=io.BytesIO(await (await aiohttp.ClientSession().get(a.url)).content.read())) for a in message.attachments],
                )

        else:
            pass

    @extension_component("_close")
    async def _session_close(self, ctx: ComponentContext):
        """When moderator chose the `Close` button."""

        _channel = await ctx.get_channel()

        result = re.findall('[0-9]+', str(_channel.name))
        user_id = _last_index(result)

        _opened = json.loads(open("./db/opened.json", "r").read())

        thread_id = _opened[str(user_id)]["thread_id"]
        msg = _opened[str(user_id)]["msg"]

        if str(ctx.channel_id) == thread_id:

            del _opened[str(user_id)]

            with open("./db/opened.json", "w") as f:
                json.dump(_opened, f, indent=4)

            await ctx.send("Closed.")

            _message = Message(
                **await self.client._http.get_message(int(thread_id), int(msg)),
                _client=self.client._http,
            )

            await _message.edit(
                content=f"Issue solved on <t:{round(datetime.datetime.utcnow().timestamp())}:F>",
                components=[],
            )

            _thread = Channel(
                **await self.client._http.get_channel(int(thread_id)),
                _client=self.client._http,
            )

            await _thread.modify(archived=True, locked=True)

            _member = Member(
                **await self.client._http.get_member(int(ctx.guild_id), int(user_id)),
                _client=self.client._http,
            )

            await _member.send("Session closed by moderator. Thank you for using Mercury.")

        else:
            pass


def setup(client) -> None:
    """Setup the Extension."""
    Modmail(client)
    print("Extension Modmail loaded.")
