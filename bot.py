"""
Root bot file.

(C) 2022 - Jimmy-Blue
"""

import os
from interactions import (
    Client,
    ClientPresence,
    Intents,
    PresenceActivity,
    CommandContext,
    PresenceActivityType,
    StatusType,
    Embed,
    EmbedFooter,
    Button,
    ButtonStyle,
)
from const import TOKEN, EXTENSION
from interactions.ext.wait_for import setup

class Bot(Client):
    """Class represents the bot client."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(
            token=TOKEN,
            intents=Intents.DEFAULT
            | Intents.GUILD_MESSAGE_CONTENT,
            presence=ClientPresence(
                activities=[
                    PresenceActivity(
                        type=PresenceActivityType.WATCHING,
                        name="for incoming mail."
                    ),
                ],
                status=StatusType.ONLINE,
            ),
        )
        self.event()(self.on_ready)

    async def on_ready(self):
        websocket = f"{self.latency * 1:.0f}"
        print("Bot is ready.")
        print(f"Latency: {websocket}ms")


client = Bot()

setup(client)

[client.load(f"exts.{ext}") for ext in EXTENSION]

@client.command(
    name="about",
    description="About Mercury.",
)
async def _about(ctx: CommandContext):

    buttons = [
        Button(
            style=ButtonStyle.LINK,
            label="Repository",
            url="https://github.com/Jimmy-Blue/Mercury",
        ),
        Button(
            style=ButtonStyle.LINK,
            label="Profile",
            url="https://blue.is-a.dev",
        ),
    ]

    embed = Embed(
        title="Mercury",
        description="".join(
            [
                "Mercury is a modmail Discord bot that members can use to get in touch with the moderation team.\n\n",
                "This project is created and maintained by Blue#2095. You can have a look at the repository",
                " and his profile by clicking on the buttons below.",
            ]
        ),
        color=0x08A46C,
        footer=EmbedFooter(
            text=f"Requested by {ctx.user.username}#{ctx.user.discriminator}",
            icon_url=ctx.user.avatar_url,
        ),
    )

    await ctx.send(embeds=embed, components=buttons)


client.start()
