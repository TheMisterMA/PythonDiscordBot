"""
File Name       :   schedule_cogs.py
Project         :   ScheduleBot
Author          :   MrMA
Creation Date   :   17.12.20

This file is defines the Cogs which group sets of commends or algorithems of the Discord's bot.
"""

from discord import ChannelType, TextChannel
from discord.ext.tasks import loop
from discord.ext.commands import Command, Bot, Cog, command
from data_handler import BotDataHandler
from constants import MY_NAME, MAIN_GUILD_ID, MAX_TIME_DELTA, BOT_LOOP_DURATION_IN_SECONDS, MAIN_CHANNEL_ID
from datetime import datetime, timezone, timedelta
import random


class Scheduling(Cog):
    """
    Command declerations for a bot in discord,
    this bot will post a callout to every member of the Guiild defined by MAIN_GUILD_ID,
    if no message is seen for the amount of time defined in MAX_TIME_DELTA,
    which is checked every amount of time defiend in BOT_LOOP_DURATION_IN_SECONDS.

    Parameters
    ----------
    bot : Bot
                    The bot which the Cog will be a part of.

    Attributes
    ----------
    last_message : Message
                    The last message been sent to the guild.

    bot : Bot
                    The bot which the Cog will be a part of.

    data_handler : BotDataHandler
                    The data handler for the data needed to be stored in the Cog for future use.
    """

    def __init__(self, bot: Bot):
        self.last_message = None
        self.bot = bot
        self.data_handler = BotDataHandler()

    @Cog.listener()
    async def on_ready(self):
        """
        Overloads the functions that get called when the client is done preparing the data received from Discord,
        usually after login is successful.
        The function prints the data about the bot which is connected, and executes the schdualing loop.
        """

        #   The info about the bot itself for admins's use.
        print(
            f"-----------------------------------------------------------------\n",
            f"--\tLogged in as:\t {self.bot.user.name}\n",
            f"--\tID number:\t {self.bot.user.id}\n",
            f"-----------------------------------------------------------------\n",
        )

        self.bots_internal_loop.start()

    @Cog.listener()
    async def on_message(self, message):
        """
        Overloads the function that get called every time a message is sent in any of the channels the bot is part of.
        This will call the super's implementation of the function and will print the info about the message.

        Parameters
        ----------
        message : Message
                        The message which the bot has detected being sent.
        """

        #   Info about the message.
        print(
            f"Got message from : {message.author.name}, {message.author.id}, in the channel : <{message.channel.name}> in <{message.channel.guild.name}>\n"
            f"\tThe Message : {message.content}"
        )
        #   TODO:   Add and integrate the dataHandler.

    @command()
    async def roll(self, ctx: TextChannel, dice: str):
        """
        Rolls a dice command, in NdN format.

        Parameters
        ----------
        ctx : TextChannel
                        The text channel in which the command was sent from.

        dice : str
                        The dice values, the amount of dices and its dimensions, in the format: NdN
        """

        try:

            #   Parses the arguments
            rolls, limit = map(int, dice.split("d"))
        except ValueError:

            #   Probably not sufficiant arguments in the chat.
            await ctx.send("Format has to be in NdN!")
            return

        #   Joins all the random rolls
        result = ", ".join(str(random.randint(1, limit)) for r in range(rolls))
        await ctx.send(result)

    @command(name="createMeeting")
    async def create_meeting(self, ctx: TextChannel, *args):
        """
        With this command you could create a meeting with the format {name} {date} {time}

        Parameters
        ----------
        name : str
                        The nameof the meeting,which has to be without any spaces of any kind.

        date : str
                        Date in the format : DD/MM/YYYY,
                        should be any valid day in the future and the present day included.

        time : str
                        Approximate time format : hh:mm,
                        if the day is the present day then the time should be in the after the current time.
        """

        if len(args) != 3:
            await ctx.send(f"Usage : {('Too much' if len(args) > 3 else 'Not enough')} arguments")
            return

        name, date, time = args

        #   TODO: add limitations for the date, so it would not add a meeting in the past.
        try:
            day, month, year = map(int, date.split("/"))
        except ValueError:
            await ctx.send("Error : Fromat has to be in DD/MM/YYYY")
            return

        #   TODO: Add limitions on the time too so it would not be in the past.
        try:
            hour, minute = map(int, time.split(":"))
        except ValueError:
            await ctx.send("Error : Fromat has to be in hh:mm")
            return

        #   Adding the meeting to the data handler
        self.data_handler.update_meetings(meeting_name=name, time=datetime(
            year=year,
            month=month,
            day=day,
            hour=hour,
            minute=minute,
            second=0,
            microsecond=0))

    @command(name="deleteMeeting")
    async def del_meeting(self, ctx: TextChannel, meeting_name: str):
        """
        Deletes a meeting that was set up, if it exist.

        Parameters
        ----------
        meeting_name : str
            The name of the meeting to be deleted.
        """

        self.data_handler.delete_meeting(meeting_name=meeting_name)

    @command(name="meetings")
    async def meeting_list(self, ctx: TextChannel):
        """
        Sends to the command's channel the list of the meetings.
        """

        for meeting_name in self.data_handler.get_meeting_names():
            await ctx.send(f"{meeting_name} in {self.data_handler.get_meetings_scheduled_time(meeting_name=meeting_name)}\n")

    #   This defines a loop that will call this function every certain amount of time.
    @loop(seconds=BOT_LOOP_DURATION_IN_SECONDS)
    async def bots_internal_loop(self):
        """
        This function is intended to be called every certain amount of time, defined in the task.loop above.
        It will execute the same functionallity when it will be called.
        """

        #   Choosing the channek intended for testing.
        for channel in self.bot.get_guild(MAIN_GUILD_ID).channels:

            #   If the current chennel is a TextChannel and it has a last message,
            #   then the variable channellast_message will not hold the last_message of that channel.
            channels_last_message = None
            if channel.type == ChannelType.text and channel.last_message_id is not None:
                channels_last_message = await channel.fetch_message(channel.last_message_id)

            #   If the above variable has a value, which is not None, the previous condtions value is true.
            #   Then, if there is no last message value in this bot or the creation time of the message is after the current last message stored,
            #   it will store the new message value.
            if channels_last_message is not None and (self.last_message == None or self.last_message.created_at < channels_last_message.created_at):
                self.last_message = channels_last_message

        #   Printing the time of creation of the last message, and the time now.
        if(self.last_message is not None):
            print(
                f"last message created at :{self.last_message.created_at.isoformat(timespec = 'microseconds')}")

        print(
            f"time now: {datetime.utcnow().isoformat(timespec = 'microseconds')}")

        #   Sending the callout message.
        if self.last_message is None or (self.last_message is not None and datetime.utcnow() - self.last_message.created_at >= MAX_TIME_DELTA):
            await self.bot.get_guild(MAIN_GUILD_ID).get_channel(MAIN_CHANNEL_ID).send("@everyone When will be the next time we meet you cunts, you didn't talk for 24 hours...")

        await self.check_meetings()

    #   Defines this will be called before the loop would start.
    @bots_internal_loop.before_loop
    async def before(self):
        """
        This function makes sure every needed configuration of the discord.py API is set.
        """
        #   Waits for all of the communications of discord to be set.
        await self.bot.wait_until_ready()

        print("Finished waiting")

    async def check_meetings(self):
        """
        Checks for the current meetings, and reminds in the main channel about the meeting, a day before, a week before and an hour before.
        """

        #   Itterates over all of the names of the meetings.
        for meeting_name in self.data_handler.get_meeting_names():

            #   The scheduled time for the meeting.
            scheduled_time = self.data_handler.get_meetings_scheduled_time(
                meeting_name=meeting_name)

            #   Checks that the time is not equal to None.
            if(scheduled_time != None):

                #   The time now, and the times to be checked with, for easier use.
                time_now = datetime.now()

                #   The time differences before the meeting, to remind of the meeting.
                time_diffrences = [
                    timedelta(hours=1),
                    timedelta(days=1),
                    timedelta(days=7)
                ]

                for time_diff in time_diffrences:
                    time_before_the_meeting = self.data_handler.get_meetings_scheduled_time(
                        meeting_name) - time_diff

                    #   If it is an hour before the meeting, and it was not reminded yet, then it will send the message.
                    if(
                            time_before_the_meeting.year == time_now.year and
                            time_before_the_meeting.month == time_now.month and
                            time_before_the_meeting.day == time_now.day and
                            time_before_the_meeting.hour == time_now.hour and
                            time_before_the_meeting.minute == time_now.minute):

                        if(self.data_handler.update_reminder(meeting_name=meeting_name, reminder=f"{'HourReminder' if time_diff == timedelta(hours=1) else 'DayReminder' if time_diff == timedelta(days=1) else 'WeekReminder'}")):

                            #   Sending the reminder to the channel.
                            await self.bot.get_guild(MAIN_GUILD_ID).get_channel(MAIN_CHANNEL_ID).send(
                                f"@everyone The meeting {meeting_name} schedualed for " +
                                f"{scheduled_time.day}/{scheduled_time.month}/{scheduled_time.year} at {scheduled_time.hour}:{scheduled_time.minute} " +
                                f"is in {'one hour' if time_diff == timedelta(hours=1) else 'tommorow' if time_diff == timedelta(days=1) else 'the next week'}"
                            )

                #   If the time now is greater then the meeting's time it will delete it automatically.
                if(time_now > self.data_handler.get_meetings_scheduled_time(meeting_name)):
                    self.data_handler.delete_meeting(meeting_name)


def setup(bot: Bot):
    """
    This function will add the Cog defined in this file to the bot that loads this file.

    Parameters
    ----------
    bot : Bot
            The bot, which the cog in this file that would be added to.
    """

    bot.add_cog(Scheduling(bot))
