"""
File Name       :   scheduleBotClient.py
Project         :   ScheduleBot
Author          :   MrMA
Creation Date   :   17.12.20    

This file is defines the client which contains the logic and algorithems of the Discord's bot.
"""

import discord
from discord.ext import tasks, commands
from constants import MY_NAME, MAIN_GUILD_ID, MAX_TIME_DELTA, BOT_LOOP_DURATION_IN_SECONDS
from dataHandler import ImportantDataHandler
from datetime import datetime, timezone
import random

class ScheduleBot(discord.ext.commands.Bot):
    """
    ScheduleBot client in discord,
    this bot will post a callout to every member of the Guiild defined by MAIN_GUILD_ID, if no message is seen for the amount of time defined in MAX_TIME_DELTA,
    which is checked every amount of time defiend in BOT_LOOP_DURATION_IN_SECONDS.
    Also it roll dice with the command '-roll' in the format NdN.
    """
    
    def __init__(self, **options):

        #   Declerations of internal members.
        self.description = '''
            This bot will callout every certain amount of time all the members encourging them to meet, if for that amount of time no messages been sent to the guild.
            Right now it doesn't do much but should in the end make the act of scheduling meetings easier and much more maneged.
        '''
        
        self.last_message = None

        #   The constructor of the discord.ext.commands.Bot class.
        super().__init__(command_prefix = '-', description = self.description)

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

        self.bots_internal_loop.start()

    async def on_message(self, message):
        """
        Overloads the function that get called every time a message is sent in any of the channels the bot is part of.
        This will call the super's implementation of the function and will print the info about the message.
        """

        #   Info about the message.
        print('Got message from : ', message.author.name, ', ', message.author.id, ' in the channel : <', message.channel.name, '> in <', message.channel.guild.name, '>') 
        print('\tThe message : ', message.content)

        #   Super's implementation of the function.
        await super().on_message(message)

        #   TODO:   Add and integrate the dataHandler.

    async def roll(self, ctx : discord.TextChannel, dice: str):
        """
        Rolls a dice in NdN format.
        """

        try:

            #   Parses the arguments
            rolls, limit = map(int, dice.split('d'))

        except Exception:

            #   Probably not sufficiant arguments in the chat.
            await ctx.send('Format has to be in NdN!')

            #   Exits the function.
            return

        #   Joins all the random rolls
        result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
        
        #   Send it back to the channel.
        await ctx.send(result)

    #   This defines a loop that will call this function every certain amount of time.
    @tasks.loop(seconds = BOT_LOOP_DURATION_IN_SECONDS)
    async def bots_internal_loop(self):
        """
        This function is intended to be called every certain amount of time, defined in the task.loop above.
        It will execute the same functionallity when it will be called.
        """

        #   Choosing the channek intended for testing.
        for channel in self.get_guild(MAIN_GUILD_ID).channels:

            #   If the current chennel is a TextChannel and it has a last message, 
            #   then the variable channellast_message will not hold the last_message of that channel.
            channelslast_message = None
            if channel.type == discord.ChannelType.text and channel.last_message != None:
                channelslast_message = await channel.fetch_message(channel.last_message.id)

            #   If the above variable has a value, which is not None, the previous condtions value is true.
            #   Then, if there is no last message value in this bot or the creation time of the message is after the current last message stored, 
            #   it will store the new message value.
            if channelslast_message != None and (self.last_message == None or self.last_message.created_at < channelslast_message.created_at):
                self.last_message = channelslast_message

        #   Printing the time of creation of the last message, and the time now. 
        if(self.last_message != None):
            print('last message created at :', self.last_message.created_at.isoformat(timespec = 'microseconds'))

        print('time now:', datetime.utcnow().isoformat(timespec = 'microseconds'))

        #   Sending the callout message.
        if (self.last_message == None or (self.last_message != None and datetime.utcnow() - self.last_message.created_at >= MAX_TIME_DELTA)):
                for channel in self.get_guild(MAIN_GUILD_ID).channels:
                    if (channel.name == 'bot-testing' and channel.type == discord.ChannelType.text):
                        await channel.send("everyone When will be the next time we meet you cunts, you didn't talk for 24 hours...")

    #   Defines this will be called before the loop would start.
    @bots_internal_loop.before_loop
    async def before(self):
        """
        This function makes sure every needed configuration of the discord.py API is set.
        """ 

        #   Waits for all of the communications of discord to be set. 
        await self.wait_until_ready()
        print("Finished waiting")