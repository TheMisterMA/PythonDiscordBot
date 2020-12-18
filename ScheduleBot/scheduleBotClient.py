import discord
from constants import MY_NAME

"""
    This class is the implementation of the, ScheduleBot client in discord.
"""
class ScheduleBotClient(discord.Client):
    async def on_ready(self):
        print('-----------------------------------------------------------------')
        print('--\tLogged in as:\t',    self.user.name)
        print('--\tID number:\t',       self.user.id)
        print('-----------------------------------------------------------------')

    async def on_message(self, message):
        #   we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return

        #   Simple Commend to check if the functionality is working.
        elif message.content.startswith('- hello'):
            print("The author :\t", message.author.name, "\tWith the ID :\t", message.author.id, "\tMessage:\t", message.content)
            await message.channel.send('Hello!')

        #   For the people who troll the bot while i test things...
        if message.content.startswith('.') and message.author.name != MY_NAME:
            print("The author :\t", message.author.name, "\tWith the ID :\t", message.author.id, "\tMessage:\t", message.content)
            await message.reply('Fuck Off You Filth', mention_author = True)
