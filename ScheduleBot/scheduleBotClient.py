"""
File Name       :   scheduleBotClient.py
Project         :   ScheduleBot
Author          :   MrMA
Creation Date   :   17.12.20

This file is defines the client which contains the logic and algorithems of the Discord's bot.
"""

import discord
from discord.ext import tasks, commands
from constants import MY_NAME, MAIN_GUILD_ID


class ScheduleBotClient(discord.Client):
    """
    This class is the implementation of the, ScheduleBot client in discord.
    """

    async def on_ready(self):
        """
        Overloads the functions that get called when the client is done preparing the data received from Discord, 
        usually after login is successful.
        The function prints the data about the bot which is connected, and executes the schdualing loop.
        """
        #   The info about the bot itself for admins's use.
        print('-----------------------------------------------------------------')
        print('--\tLogged in as:\t',    self.user.name)
        print('--\tID number:\t',       self.user.id)
        print('-----------------------------------------------------------------')

        #   Executing the schdual loop.
        self.called_once_a_day().start()

    async def on_message(self, message):
        """
        This function overloads the function that get called by discord.py when a message 
        is sent in one of the channels the bot has access to.
        It will ignore every message the bot himself sends.
        For the message '- hello' it will send a simple 'Hello!' to the same channel the other message was sent.
        If the message will start with 'עד מתי' or 'כמה עוד' it will return an IDF small joke.
        And if someone other then me will send anything that will start with '.' it will curse to avoid trolls.
        """
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

    #   This defines a loop that will call this function every certain amount of time.
    @tasks.loop(minutes=1)
    async def called_once_a_day(self):
        """
        This function is intended to be called every certain amount of time, defined in the task.loop above.
        It will execute the same functionallity when it will be called.
        """

        #   Choosing the channek intended for testing.
        for channel in self.get_guild(MAIN_GUILD_ID).channels:
            if (channel.name == 'bot-testing'):
                message_channel = channel

        #   Print the channel information
        print(f"Got channel {message_channel}")

        #   Sending to that channel a message to check if this function get called every loop.
        await message_channel.send("Loop check")

    #   Defines this will be called before the loop would start.
    @called_once_a_day.before_loop
    async def before(self):
        """
        This function makes sure every needed configuration of the discord.py API is set.
        """

        #   Waits for all of the communications of discord to be set. 
        await self.wait_until_ready()
        print("Finished waiting")