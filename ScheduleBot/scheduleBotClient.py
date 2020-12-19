import discord
from discord.ext import tasks, commands
from constants import MY_NAME, MAIN_GUILD_ID

"""
    This class is the implementation of the, ScheduleBot client in discord.
"""
class ScheduleBotClient(discord.Client):
    async def on_ready(self):
        print('-----------------------------------------------------------------')
        print('--\tLogged in as:\t',    self.user.name)
        print('--\tID number:\t',       self.user.id)
        print('-----------------------------------------------------------------')

        @tasks.loop(minutes=1)
        async def called_once_a_day():
            for channel in self.get_guild(MAIN_GUILD_ID).channels:
                if (channel.name == 'bot-testing'):
                    message_channel = channel

            print(f"Got channel {message_channel}")

            await message_channel.send("Loop check")

        @called_once_a_day.before_loop
        async def before():
            await self.wait_until_ready()
            print("Finished waiting")

        called_once_a_day.start()

    async def on_message(self, message):
        #   we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return

        #   Simple Commend to check if the functionality is working.
        elif message.content.startswith('- hello'):
            print("The author :\t", message.author.name, "\tWith the ID :\t", message.author.id, "\tMessage:\t", message.content)
            await message.channel.send('Hello!')
        
        #   Frequent army phrases that will be funny.
        elif message.content.startswith('עד מתי'):
            print("The author :\t", message.author.name, "\tWith the ID :\t", message.author.id, "\tMessage:\t", message.content)
            await message.reply('עד מתי שפאקינג צריך נבלה')

        elif message.content.startswith('כמה עוד'):
            print("The author :\t", message.author.name, "\tWith the ID :\t", message.author.id, "\tMessage:\t", message.content)
            await message.reply('כמה שעוד צריך יא חלאה...')

        #   For the people who troll the bot while i test things...
        if message.content.startswith('.') and message.author.name != MY_NAME:
            print("The author :\t", message.author.name, "\tWith the ID :\t", message.author.id, "\tMessage:\t", message.content)
            await message.reply('Fuck Off You Filth', mention_author = True)
