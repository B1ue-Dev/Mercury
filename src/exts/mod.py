import interactions
from interactions import extension_command as command
import os, json
from dotenv import load_dotenv
load_dotenv()
SCOPE = int(os.getenv('SCOPE'))





class Mod(interactions.Extension):
    def __init__(self, client: interactions.Client):
        self.client: interactions.Client = client

    @command(
        name="modmail",
        description="Moderation command for the bot",
        scope=SCOPE,
        options=[
            interactions.Option(
                type=interactions.OptionType.SUB_COMMAND,
                name="block",
                description="Block a user from using the bot",
                options=[
                    interactions.Option(
                        type=interactions.OptionType.USER,
                        name="user",
                        description="The user to block",
                        required=True
                    ),
                    interactions.Option(
                        type=interactions.OptionType.STRING,
                        name="reason",
                        description="The reason for blocking the user",
                        required=True
                    ),
                ],
            ),
            interactions.Option(
                type=interactions.OptionType.SUB_COMMAND,
                name="unblock",
                description="Unblock a user from using the bot",
                options=[
                    interactions.Option(
                        type=interactions.OptionType.USER,
                        name="user",
                        description="The user to unblock",
                        required=True
                    ),
                ],
            ),
            interactions.Option(
                type=interactions.OptionType.SUB_COMMAND,
                name="list",
                description="List blocked users",
            ),
            interactions.Option(
                type=interactions.OptionType.SUB_COMMAND,
                name="check",
                description="Check if a user is blocked",
                options=[
                    interactions.Option(
                        type=interactions.OptionType.USER,
                        name="user",
                        description="The user to check",
                        required=True
                    )
                ]
            )
        ],
        default_member_permissions=interactions.Permissions.KICK_MEMBERS,
        dm_permission=False,
    )
    async def _modmail(self, ctx: interactions.CommandContext,
        sub_command: str,
        user: interactions.Member = None,
        reason: str = None
    ):
        if sub_command == "block":
            await self._modmail_block(ctx, user, reason)
        elif sub_command == "unblock":
            await self._modmail_unblock(ctx, user)
        elif sub_command == "list":
            await self._modmail_list(ctx)
        elif sub_command == "check":
            await self._modmail_check(ctx, user)


    async def _modmail_block(self, ctx: interactions.CommandContext, user: interactions.Member, reason: str):
        user_id = str(user.user.id)
        _blocked_list = json.loads(open("./db/blocked.json", "r").read())
        if str(user_id) in _blocked_list:
            await ctx.send(f"{user.mention} is already blocked.", ephemeral=True)
        else:
            _blocked_list[user_id] = {
                "reason": reason,
                "blocked_by": str(ctx.author.id)
            }
            with open("./db/blocked.json", "w") as f:
                json.dump(_blocked_list, f, indent=4)
            await ctx.send(f"{user.mention} was blocked.")


    async def _modmail_unblock(self, ctx: interactions.CommandContext, user: interactions.Member):
        user_id = str(user.user.id)
        _blocked_list = json.loads(open("./db/blocked.json", "r").read())
        if str(user_id) in _blocked_list:
            del _blocked_list[user_id]
            with open("./db/blocked.json", "w") as f:
                json.dump(_blocked_list, f, indent=4)
            await ctx.send(f"{user.mention} was unblocked.")
        else:
            await ctx.send(f"{user.mention} was not blocked.", ephemeral=True)


    async def _modmail_list(self, ctx: interactions.CommandContext):
        _blocked_list = json.loads(open("./db/blocked.json", "r").read())
        if len(_blocked_list) == 0:
            await ctx.send("No blocked user.", ephemeral=True)
        else:
            embed = interactions.Embed(
                title="".join("Blocked users:" if len(_blocked_list) > 1 else "Block user:"),
                description="\n".join([
                    f"<@{user_id}>: {_blocked_list[user_id]['reason']}"
                    for user_id in _blocked_list
                ])
            )
            await ctx.send(embeds=embed)


    async def _modmail_check(self, ctx: interactions.CommandContext, user: interactions.Member):
        user_id = str(user.user.id)
        _blocked_list = json.loads(open("./db/blocked.json", "r").read())
        if str(user_id) not in _blocked_list:
            await ctx.send(f"{user.mention} was not blocked.", ephemeral=True)
        else:
            thumbnail = interactions.EmbedImageStruct(url=user.user.avatar_url)
            fields = [
                interactions.EmbedField(name="Reason", value=_blocked_list[user_id]['reason'], inline=True),
                interactions.EmbedField(name="Moderator", value=f"<@{_blocked_list[user_id]['blocked_by']}>", inline=True)
            ]
            embed = interactions.Embed(
                title=f"{user.user.username}#{user.user.discriminator}",
                description=f"<@{user.user.id}>",
                thumbnail=thumbnail,
                fields=fields
            )
            await ctx.send(embeds=embed)


def setup(client):
    Mod(client)
