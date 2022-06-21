"""
Root bot file.

(C) 2022 - Jimmy-Blue
"""

import os
import interactions
from const import TOKEN

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

client.start()
