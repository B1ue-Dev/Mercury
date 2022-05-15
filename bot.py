import interactions
import os
from dotenv import load_dotenv
load_dotenv()
bot_token = os.getenv('TOKEN')



bot = interactions.Client(bot_token,
	intents=interactions.Intents.ALL,
	#disable_sync=True
)


bot.load('exts.mod')
bot.load('exts.modmail')



@bot.event
async def on_ready():
	websocket = f"{bot.latency * 1:.0f}"
	print('Bot is ready.')
	print(f'Latency: {websocket}ms')






bot.start()
