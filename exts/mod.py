import interactions
from interactions import extension_command as command
import os, json
from dotenv import load_dotenv
load_dotenv()


_blocked_list = {}


class Mod(interactions.Extension):
	def __init__(self, bot) -> None:
		super().__init__()
		self.bot = bot
	

	@command(
		name="modmail",
		description="Moderation command for the bot",
		scope=738938246574374913,
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
		if sub_command == "unblock":
			await self._modmail_unblock(ctx, user)
			
		

	async def _modmail_block(self, ctx: interactions.CommandContext, user: interactions.Member, reason: str):
		user_id = str(user.user.id)
		_blocked_list = json.loads(open("./db/blocked.json", "r").read())
		if str(user_id) in _blocked_list:
			await ctx.send(f"{user.mention} is already blocked")
		else:
			_blocked_list[user_id] = {
				"reason": reason,
				"blocked_by": str(ctx.author.id)
			}
			with open("./db/blocked.json", "w") as f:
				json.dump(_blocked_list, f, indent=4)
			await ctx.send(f"{user.mention} has been blocked")
	

	async def _modmail_unblock(self, ctx: interactions.CommandContext, user: interactions.Member):
		user_id = str(user.user.id)
		_blocked_list = json.loads(open("./db/blocked.json", "r").read())
		if str(user_id) in _blocked_list:
			del _blocked_list[user_id]
			with open("./db/blocked.json", "w") as f:
				json.dump(_blocked_list, f, indent=4)
			await ctx.send(f"{user.mention} has been unblocked")
		else:
			await ctx.send(f"{user.mention} is not blocked")
			







def setup(bot):
	Mod(bot)
