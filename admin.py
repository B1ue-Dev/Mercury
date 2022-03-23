import nextcord
from nextcord.ext import commands



class Commands(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	@commands.command(name="block")
	@commands.has_permissions(kick_members=True)
	"""
	Command: block
	Usage: Block a member from using the modmail bot.
	"""
	async def block(self, ctx, member: nextcord.Member):
		ids = str(member.id)
		with open("./data/blocked.txt", "a+") as f:
			data1 = f"{ids},"
			f.write(f"{data1}")
		with open("./data/blocked_read.txt", "a+") as s:
			data2 = f"<@!{ids}>,"
			s.write(f"{data2}")
		await ctx.send("{} has been blocked.".format(member))


	@commands.command(name="unblock")
	@commands.has_permissions(kick_members=True)
	"""
	Command: unblock
	Usage: Unblock a member from using the modmail bot.
	"""
	async def unblock(self, ctx, member: nextcord.Member):
		ids = str(member.id)
		with open("./data/blocked.txt", "r") as f:
			data1 = f.read()
			data1 = data1.replace(f"{ids},", "")
		with open("./data/blocked.txt", "w") as f:
			f.write(data1)
		with open("./data/blocked_read.txt", "r") as s:
			data2 = s.read()
			data2 = data2.replace(f"<@!{ids}>,", "")
		with open("./data/blocked_read.txt", "w") as s:
			s.write(data2)
		await ctx.send("{} has been unblocked.".format(member))


	@commands.command(name="check")
	@commands.has_permissions(kick_members=True)
	"""
	Command: check
	Usage: Check whenever a member is blocked/unblocked.
	"""
	async def check(self, ctx, member: nextcord.Member):
		with open("./data/blocked.txt", "r") as f:
			data = f.read()
			if str(member.id) in data:
				await ctx.send("{} is blocked.".format(member))
			else:
				await ctx.send("{} is not blocked.".format(member))


	@commands.command(name="list")
	@commands.has_permissions(kick_members=True)
	"""
	Command: list
	Usage: Shows a list of blocked members.
	"""
	async def list(self, ctx):
		with open("./data/blocked_read.txt", "r") as f:
			data2 = f.read()
			data2 = data2.replace(",", "\n")
			try:
				await ctx.send(data2)
			except nextcord.errors.HTTPException:
				await ctx.send("No one is blocked.")
		







def setup(bot):
	bot.add_cog(Commands(bot))