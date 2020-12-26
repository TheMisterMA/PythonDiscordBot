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
from dataHandler import ImportantDataHandler
from datetime import datetime, timezone, timedelta
import random

class ScheduleBot(discord.ext.commands.Bot):
    """
    This class is the implementation of the, ScheduleBot client in discord.
    """
    
    def __init__(self, **options):

        #   Declerations of internal members.
        self.description = '''
            This bot should do small actions.
            Right now it doesn't do much but should in the end make the act of scheduling meetings easier and much more maneged.
        '''

        #   self.importentData = ImportantDataHandler()
        self.lastMessage = None

        #   The constructor of the discord.ext.commands.Bot class.
        super().__init__(command_prefix='-', description=self.description)

        #   Adding the functions of this class as commands for the bots.
        self.add_command(commands.Command(self.roll))

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

        self.botsInternalLoop.start()

    async def on_message(self, message):
        print('Got message from : ', message.author.name, ', ', message.author.id, ' in the channel : <', message.channel.name, '> in <', message.channel.guild.name , '>\n\tThe message : ', message.content)
        await super().on_message(message)

        #self.importentData.updateLastMessage(message)

    async def roll(self, ctx : discord.TextChannel, dice: str):
        """
        Rolls a dice in NdN format.
        """

        try:
            rolls, limit = map(int, dice.split('d'))
        except Exception:
            await ctx.send('Format has to be in NdN!')
            return

        result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
        await ctx.send(result)

    #   This defines a loop that will call this function every certain amount of time.
    @tasks.loop(seconds=3)
    async def botsInternalLoop(self):
        """
        This function is intended to be called every certain amount of time, defined in the task.loop above.
        It will execute the same functionallity when it will be called.
        """

        #   Choosing the channek intended for testing.
        for channel in self.get_guild(MAIN_GUILD_ID).channels:
            if channel.type == discord.ChannelType.text and channel.last_message != None:
                channelsLastMessage = await channel.fetch_message(channel.last_message.id)

            if (
                channel.type == discord.ChannelType.text and 
                channel.last_message != None and (
                    self.lastMessage == None or (
                        self.lastMessage.created_at > channelsLastMessage.created_at and 
                        self.user.id != channelsLastMessage.author.id
                    )
                )
            ):
                self.lastMessage = await channel.fetch_message(channel.last_message.id)

        print('Last message is None : ', self.lastMessage != None)
        
        if(self.lastMessage != None):
            print('last message created at :', self.lastMessage.created_at.isoformat(timespec = 'microseconds'))

        print('time now:', datetime.now(timezone.utc).isoformat(timespec = 'microseconds'))

        if (self.lastMessage != None and datetime.now() - self.lastMessage.created_at >= timedelta(hours = 2, minutes=1)):
                print('CHECKED')
                for channel in self.get_guild(MAIN_GUILD_ID).channels:
                    if (channel.name == 'bot-testing' and channel.type == discord.ChannelType.text):
                        await channel.send("everyone When will be the next time we meet you cunts, you didn't talk for 24 hours...")
        #elif (self.lastMessage == None):
        #    for channel in self.get_guild(MAIN_GUILD_ID).channels:
        #        if (channel.name == 'bot-testing' and channel.type == discord.ChannelType.text):
        #            await channel.send("everyone When will be the next time we meet you cunts, you didn't talk for 24 hours...")

    #   Defines this will be called before the loop would start.
    @botsInternalLoop.before_loop
    async def before(self):
        """
        This function makes sure every needed configuration of the discord.py API is set.
        """ 
        #   Waits for all of the communications of discord to be set. 
        await self.wait_until_ready()
        print("Finished waiting")