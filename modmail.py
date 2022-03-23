from nextcord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
channel_id = int(os.getenv("CHANNEL_ID"))

class Modmail(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_message(self, message):
		empty_array = []

		modmail_channel = await self.bot.fetch_channel(channel_id)
		
		# Check if member is in blocked list
		fp = open('./data/blocked.txt')
		bad_list = [word.strip() for line in fp.readlines() for word in line.split(',') if word.strip()]
		if str(message.author.id) in bad_list:
			fp.close()
			return
		else:
				if message.author.id == self.bot.user.id:
					return
				if str(message.channel.type) == "private":
					if message.attachments != empty_array:
						files = message.attachments
						await modmail_channel.send(content=("<@" + str(message.author.id) + ">: " + message.content))
						for file in files:
							await modmail_channel.send(file.url)
					else:
						await modmail_channel.send(content=("<@" + str(message.author.id) + ">: " + message.content))


				elif str(message.channel.id) == channel_id and message.content.startswith("<"):
					member_object = message.mentions[0]
					if message.attachments != empty_array:
						files = message.attachments
						await member_object.send("**" + str(message.author) + "**" + ": " + message.content)
						for file in files:
							await member_object.send(file.url)
					else:
						index = message.content.index(" ")
						string = message.content
						mod_message = string[index:]
						await member_object.send("**" + str(message.author) + "**" + ": " + mod_message)





def setup(bot):
	bot.add_cog(Modmail(bot))
