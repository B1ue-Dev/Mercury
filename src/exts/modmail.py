"""
Modmail system handler.

(C) 2022 - Jimmy-Blue
"""

import json
import interactions
from const import MODMAIL_CHANNEL


class Modmail(interactions.Extension):
    def __init__(self, client: interactions.Client):
        self.client: interactions.Client = client

    @interactions.extension_listener(name="on_message_create")
    async def _message_create(self, message: interactions.Message):
        channel = await message.get_channel()

        if channel.type == interactions.ChannelType.DM:
            if int(message.author.id) == int(self.client.me.id):
                return

            user_id = str(message.author.id)
            _blocked_list = json.loads(open("./db/blocked.json", "r").read())
            if str(user_id) in _blocked_list:
                return

            _channel = interactions.Channel(**await self.client._http.get_channel(MODMAIL_CHANNEL), _client=self.client._http)
            _content = message.content
            _replied = None

            if message.referenced_message:
                if len(message.referenced_message['content']) > 71:
                    _replied = message.referenced_message['content'][:70] + "..."
                else:
                    _replied = message.referenced_message['content']

            if _replied:
                await _channel.send(f"{message.author.mention}\n> {_replied}\n{_content}")
                if message.attachments:
                    for attachment in message.attachments:
                        await _channel.send(attachment.url)
            else:
                await _channel.send(f"{message.author.mention}\n{_content}")
                if message.attachments:
                    for attachment in message.attachments:
                        await _channel.send(attachment.url)

        elif channel.type == interactions.ChannelType.GUILD_TEXT:
            if message.referenced_message and message.referenced_message['type'] == 0:
                try:
                    _member_mentions = message.referenced_message['mentions'][0]
                    _member = interactions.Member(**await self.client._http.get_member(guild_id=str(message.guild_id), member_id=str(_member_mentions['id'])), _client=self.client._http)
                    _content = message.content

                    await _member.send(f"{_content}")
                    if message.attachments:
                        for attachment in message.attachments:
                            await _member.send(attachment.url)
                
                except IndexError:
                    pass
            
            elif message.content.startswith("("):
                ...

        else:
            return


def setup(client):
    Modmail(client)
