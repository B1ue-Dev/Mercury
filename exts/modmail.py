import interactions
from interactions import extension_listener as listener
import os, json
from dotenv import load_dotenv
load_dotenv()
MODMAIL_CHANNEL = int(os.getenv('MODMAIL_CHANNEL'))





class Modmail(interactions.Extension):
	def __init__(self, bot) -> None:
		super().__init__()
		self.bot = bot


	@listener(name="on_message_create")
	async def _message_create(self, message: interactions.Message):
		channel = await message.get_channel()

		if channel.type == interactions.ChannelType.DM:
			if int(message.author.id) == int(self.bot.me.id):
				return
			else:
				_channel = interactions.Channel(**await self.bot._http.get_channel(MODMAIL_CHANNEL), _client=self.bot._http)
				await _channel.send(f"{message.author.username}#{message.author.discriminator}: {message.content}")
				if message.attachments:
					for attachment in message.attachments:
						await _channel.send(attachment.url)

		elif channel.type == interactions.ChannelType.GUILD_TEXT:
			if int(message.channel_id) == int(MODMAIL_CHANNEL) and message.content.startswith("<"):
				if int(message.author.id) == int(self.bot.me.id):
					return
				else:
					_member_object = message.mentions[0]
					_member = interactions.Member(**await self.bot._http.get_member(guild_id=int(message.guild_id), member_id=int(_member_object['id'])), _client=self.bot._http)
					_content = message.content.replace(f"<@{_member_object['id']}>", "")
					await _member.send(f"{_content}")
					if message.attachments:
						for attachment in message.attachments:
							await _member.send(attachment.url)

		else:
			return





def setup(bot):
	Modmail(bot)
