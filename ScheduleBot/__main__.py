#!/usr/bin/env python3

"""
File Name       :   __main__.py
Project         :   ScheduleBot
Author          :   MrMA
Creation Date   :   17.12.20

This file is a script, which executes the bot client in discord.
"""

from discord.ext.commands import Bot
from constants import BOT_TOKEN

description = """
    This bot will callout every certain amount of time all the members encourging them to meet, if for that amount of time no messages been sent to the guild.
    Right now it doesn't do much but should in the end make the act of scheduling meetings easier and much more maneged.
    """

#   Creating the BotClient
client = Bot(command_prefix="-", description=description)

client.load_extension("scheduleBotClient")

#   Run the Bot Client with the Token of the specific bot created for this program.
client.run(BOT_TOKEN)
