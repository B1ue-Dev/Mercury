import interactions
import os
from dotenv import load_dotenv
load_dotenv()
bot_token = os.getenv('TOKEN')



bot = interactions.Client(
	token=bot_token,
	intents=interactions.Intents.ALL,
	presence=interactions.ClientPresence(
		activities=[
			interactions.PresenceActivity(
				type=interactions.PresenceActivityType.WATCHING,
				name="for incoming modmail"
			)
		],
		status=interactions.StatusType.ONLINE,
	)
)


bot.load('exts.mod')
bot.load('exts.modmail')



@bot.event
async def on_ready():
	websocket = f"{bot.latency * 1:.0f}"
	print('Bot is ready.')
	print(f'Latency: {websocket}ms')
	await bot.change_presence(
		interactions.ClientPresence(
			activities=[
				interactions.PresenceActivity(
					type=interactions.PresenceActivityType.WATCHING,
					name="for incoming modmail"
				)
			],
			status=interactions.StatusType.ONLINE,
		)
	)






bot.start()
