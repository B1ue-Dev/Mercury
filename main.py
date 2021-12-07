import discord
from discord.ext import commands
import json


with open('./data/config.json') as f:
	data = json.load(f)

bot = commands.Bot(command_prefix="!")

bot.load_extension('modmail')

@bot.event
async def on_ready():
	game = discord.Game("Waiting for incoming modmail")
	await bot.change_presence(status=discord.Status.online, activity=game)
	print("Bot is ready!")


bot.run(data['TOKEN'])