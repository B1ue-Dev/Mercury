import nextcord
from nextcord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
scope = os.getenv("TOKEN")



intents = nextcord.Intents.default()
intents.members = True
activity = nextcord.Activity(type=nextcord.ActivityType.watching, name="for incoming modmail")
bot = commands.Bot(command_prefix="m!", activity=activity, intents=intents, help_command=None)



bot.load_extension('jishaku')
bot.load_extension('modmail')
bot.load_extension('admin')



@bot.event
async def on_ready():
	print("Bot is ready!")





bot.run(scope)
