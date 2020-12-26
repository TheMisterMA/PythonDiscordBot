"""
File Name       :   __main__.py
Project         :   ScheduleBot
Author          :   MrMA
Creation Date   :   17.12.20

This file is a script, which executes the bot client in discord.
"""

import discord
from discord.ext import tasks, commands
from scheduleBotClient import ScheduleBot
from constants import BOT_TOKEN, MAIN_GUILD_ID

#   Creating the BotClient
client = ScheduleBot()

#   Run the Bot Client with the Token of the specific bot created for this program.
client.run(BOT_TOKEN)