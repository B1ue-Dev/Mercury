"""
Moderation commands.

(C) 2022 - Jimmy-Blue
"""

import json
from interactions import (
    extension_command,
    option,
    Extension,
    Client,
    CommandContext,
    OptionType,
    Permissions,
    Member,
    Embed,
    EmbedImageStruct,
    EmbedField,
)
from const import SCOPE


class Mod(Extension):
    """Moderation commands for Mercury."""

    def __init__(self, client: Client) -> None:
        self.client: Client = client

    @extension_command(
        scope=SCOPE,
        default_member_permissions=Permissions.KICK_MEMBERS,
    )
    async def modmail(self, *args, **kwargs):
        ...

    @modmail.subcommand()
    @option(
        description="The user you wish to block.",
        type=OptionType.USER,
        required=True,
    )
    @option(
        description="The reason for the action.",
        required=False,
    )
    async def block(self, ctx: CommandContext, user: Member, reason: str = "N/A"):
        """Block a user from using Mercury."""

        user_id = str(user.user.id)

        _blocked = json.loads(open("./db/blocked.json", "r").read())

        if user_id in _blocked:
            return await ctx.send(f"{user.mention} is already blocked.", ephemeral=True)

        _blocked[user_id] = {
            "reason": reason,
            "blocked_by": str(ctx.author.id)
        }

        with open("./db/blocked.json", "w") as f:
            json.dump(_blocked, f, indent=4)

        await ctx.send(f"{user.mention} was blocked.")

    @modmail.subcommand()
    @option(
        description="The user you wish to unblock.",
    )
    async def unblock(self, ctx: CommandContext, user: Member):
        """Unblock a user from using Mercury."""

        user_id = str(user.user.id)

        _blocked = json.loads(open("./db/blocked.json", "r").read())

        if user_id not in _blocked:
            return await ctx.send(f"{user.mention} was not blocked.", ephemeral=True)

        del _blocked[user_id]

        with open("./db/blocked.json", "w") as f:
            json.dump(_blocked, f, indent=4)

        await ctx.send(f"{user.mention} was unblocked.")

    @modmail.subcommand()
    async def list(self, ctx: CommandContext):
        """List all blocked users."""

        _blocked = json.loads(open("./db/blocked.json", "r").read())

        if len(_blocked) == 0:
            return await ctx.send("No blocked user.", ephemeral=True)

        embed = Embed(
            title="".join("Blocked users:" if len(_blocked) > 1 else "Block user:"),
            description="\n".join(
                [
                    f"<@{user_id}>: {_blocked[user_id]['reason']}"
                    for user_id in _blocked
                ]
            )
        )

        await ctx.send(embeds=embed)

    @modmail.subcommand()
    async def check(self, ctx: CommandContext, user: Member):
        """Check if a user is blocked from Mercury."""

        user_id = str(user.user.id)

        _blocked = json.loads(open("./db/blocked.json", "r").read())

        if user_id not in _blocked:
            return await ctx.send(f"{user.mention} was not blocked.", ephemeral=True)

        thumbnail = EmbedImageStruct(url=user.user.avatar_url)
        fields = [
            EmbedField(
                name="Reason",
                value=_blocked[user_id]['reason'],
                inline=True,
            ),
            EmbedField(
                name="Moderator",
                value=f"<@{_blocked[user_id]['blocked_by']}>",
                inline=True,
            )
        ]
        embed = Embed(
            title=f"{user.user.username}#{user.user.discriminator}",
            description=f"<@{user.user.id}>",
            thumbnail=thumbnail,
            fields=fields,
        )

        await ctx.send(embeds=embed)


def setup(client) -> None:
    """Setup the Extension."""
    Mod(client)
    print("Extension Mod loaded.")
