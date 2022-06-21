"""
Root bot file.

(C) 2022 - Jimmy-Blue
"""

import os
import interactions
from const import TOKEN, SCOPE

client = interactions.Client(
    token=TOKEN,
    intents=interactions.Intents.DEFAULT | interactions.Intents.GUILD_MESSAGE_CONTENT,
    presence=interactions.ClientPresence(
        activities=[
            interactions.PresenceActivity(
                type=interactions.PresenceActivityType.WATCHING,
                name="for incoming mail"
            )
        ],
        status=interactions.StatusType.ONLINE,
    )
)

[client.load(f"exts.{ext}") for ext in [file.replace(".py", "") for file in os.listdir("exts") if not file.startswith("_")]]

@client.event
async def on_ready():
    websocket = f"{client.latency * 1:.0f}"
    print('Bot is ready.')
    print(f'Latency: {websocket}ms')

@client.command(
    name="about",
    description="About Mercury",
    scope=SCOPE,
)
async def _about(ctx: interactions.CommandContext):
    embed = interactions.Embed(
        title="Mercury",
        description="Mercury is a modmail Discord bot that members can use to get in touch with the moderation team.\n\nThis project is created and maintained by Blue#2095. You can have a look at the repository and his profile by clicking on the buttons below.",
        color=0x08a46c,
        footer=interactions.EmbedFooter(
            text=f"Requested by {ctx.user.username}#{ctx.user.discriminator}",
            icon_url=ctx.user.avatar_url
        )
    )

    buttons = [
        interactions.Button(
            style=interactions.ButtonStyle.LINK,
            label="Repository",
            url="https://github.com/Jimmy-Blue/Mercury"
        ),
        interactions.Button(
            style=interactions.ButtonStyle.LINK,
            label="Profile",
            url="https://blue.is-a.dev"
        )
    ]

    await ctx.send(embeds=embed, components=buttons)

client.start()
