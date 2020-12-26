"""
File Name       :   scheduleBotClient.py
Project         :   ScheduleBot
Author          :   MrMA
Creation Date   :   17.12.20

This file defines the Bot's data handler, with it the bot could menege and stroe data more efficiently
"""

from json import dump
from discord import Message


class BotDataHandler(object):
    """
    This class will handle certain information the bot needs to use even if it will go down.
    """

    def __init__(self, file_path: str = "Data.json"):
        self.data = {}
        self.file_path = file_path

    def updateLastMessage(self, message: Message):

        self.data["LastMessage"] = {
            "Constent":   f"{message.content}",
            "AuthorName":   f"{message.author.name}",
            "MessageID":   f"{message.id}",
            "GuildID":   f"{message.guild.id}",
            "CreationDate":   {
                "Year":   f"{message.created_at.year}",
                "Month":   f"{message.created_at.month}",
                "Day":   f"{message.created_at.day}",
                "Hour":   f"{message.created_at.hour}",
                "Minute":   f"{message.created_at.minute}",
                "Second":   f"{message.created_at.second}"
            }
        }

        with open(self.file_path, "w") as json_file:
            dump(self.data, json_file)
