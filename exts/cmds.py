"""
Commands for modmail.

(C) 2022 - Jimmy-Blue
"""

import json
import datetime
from interactions import (
    extension_command,
    extension_modal,
    Extension,
    Client,
    CommandContext,
    Message,
    Channel,
    ChannelType,
    Embed,
    EmbedFooter,
    Button,
    ButtonStyle,
    Modal,
    TextInput,
    TextStyleType,
)
from const import MODMAIL_CHANNEL, MOD_ROLE


class Cmds(Extension):
    def __init__(self, client: Client) -> None:
        self.client: Client = client

    @extension_command(
        name="create",
        description="Create a new modmail session.",
    )
    async def _create(self, ctx: CommandContext):
        """/create Create a new modmail session."""

        _blocked = json.loads(open("./db/blocked.json", "r").read())

        if str(ctx.user.id) in _blocked:
            return await ctx.send("You were blocked from using Mercury.", ephemeral=True)

        _opened = json.loads(open("./db/opened.json", "r").read())

        if str(ctx.user.id) in _opened:
            return await ctx.send(
                content="".join(
                    [
                        "You already have a session opened.\n",
                        "Use `/close` to close the current session and start a new one."
                    ]
                )
            )

        _modal = Modal(
            title="New modmail session",
            custom_id="new_session",
            components=[
                TextInput(
                    style=TextStyleType.PARAGRAPH,
                    label="Type your issue below",
                    placeholder="(Ex) I have a problem with a member from the server...",
                    custom_id="_issue",
                    max_length=2000,
                )
            ]
        )

        await ctx.popup(_modal)

    @extension_command(
        name="close",
        description="Close the current modmail session.",
    )
    async def _close(self, ctx: CommandContext):
        """/close Close the current modmail session."""

        thread_id = None
        msg = None

        _opened = json.loads(open("./db/opened.json", "r").read())

        if str(ctx.user.id) not in _opened:
            return await ctx.send("You do not have any session opened at the moment", ephemeral=True)

        thread_id = _opened[str(ctx.user.id)]["thread_id"]
        msg = _opened[str(ctx.user.id)]["msg"]

        del _opened[str(ctx.user.id)]

        with open("./db/opened.json", "w") as f:
            json.dump(_opened, f, indent=4)

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

        await ctx.send("Current session closed. Thank you for using Mercury.", ephemeral=True)

    @extension_modal("new_session")
    async def _new_session(self, ctx: CommandContext, _issue: str):
        """Event callback for new_session Modal()."""

        _opened = json.loads(open("./db/opened.json", "r").read())

        await ctx.send("Session created. Head over to my DM to start the conversation.", ephemeral=True)

        _help_thread = Channel(
            **await self.client._http.create_thread(
                channel_id=MODMAIL_CHANNEL,
                name=f"{ctx.user.username}-{ctx.user.id}",
                auto_archive_duration=4320,
                thread_type=ChannelType.GUILD_PUBLIC_THREAD,
                invitable=False,
                reason="N/A",
            ),
            _client=self.client._http,
        )

        _msg = await _help_thread.send(
            content=f"<@&{MOD_ROLE}>\nOnce the issue is solve, please press the `Close` button below to close the session.",
            embeds=Embed(
                title=f"From {ctx.user.username}#{ctx.user.discriminator}",
                description=f"{_issue}",
                color=0x08A46C,
                footer=EmbedFooter(text=f"ID: {int(ctx.user.id)}"),
                timestamp=datetime.datetime.utcnow(),
            ),
            allowed_mentions={"parse": ["roles", "everyone"]},
            components=[
                Button(
                    style=ButtonStyle.DANGER,
                    label="Close",
                    custom_id="_close",
                )
            ]
        )
        await _msg.pin()

        _opened[str(ctx.user.id)] = {
            "issue": _issue,
            "thread_id": str(_help_thread.id),
            "msg": str(_msg.id)
        }

        with open("./db/opened.json", "w") as f:
            json.dump(_opened, f, indent=4)


def setup(client) -> None:
    """Setup the Extension."""
    Cmds(client)
    print("Extension Cmds loaded.")
