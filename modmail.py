from discord.ext import commands
import json


with open('./data/config.json') as f:
    data = json.load(f)


class Modmail(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        empty_array = []
        channel_id = data['CHANNEL_ID']
        modmail_channel = await self.bot.fetch_channel(channel_id)

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