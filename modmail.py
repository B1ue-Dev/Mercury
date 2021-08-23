from discord.ext import commands
import data # Take the data in data.py


class Modmail(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        empty_array = []
        modmail_channel = await self.bot.fetch_channel(data.CHANNEL_ID)

        if message.author.id == self.bot.user.id:
            return
        if str(message.channel.type) == "private":
            if message.attachments != empty_array:
                files = message.attachments
                await modmail_channel.send(content=("<@" + message.author.id + ">: "))


                for file in files:
                    await modmail_channel.send(file.url)
            else:
                await modmail_channel.send(content=("<@" + str(message.author.id) + ">: " + message.content))

        elif str(message.channel) == modmail_channel and message.content.startswith("<"):
            member_object = message.mentions[0]
            if message.attachments != empty_array:
                files = message.attachments
                await member_object.send("**[MOD]** " + "**" + message.author.display_name + "**: ")

                for file in files:
                    await member_object.send(file.url)
            else:
                index = message.content.index(" ")
                string = message.content
                mod_message = string[index:]
                await member_object.send("**[MOD]** " + "**" + message.author.display_name + "**: " + mod_message)

def setup(bot):
    bot.add_cog(Modmail(bot))
