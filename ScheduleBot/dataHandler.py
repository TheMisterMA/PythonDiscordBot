import json
import discord

class importantDataHandler(object):
    """
    docstring
    """
    def __init__(self):
        self.data = {}

    def updateLastMessage(self, message : discord.Message):
        self.data['LastMessage'] = {
            'Constent'      :   message.content,
            'AuthorName'    :   message.author.name,
            'MessageID'     :   message.id,
            'GuildID'       :   message.guild.id,
            'CreationDate'  :   {
                'Year'          :   str(message.created_at.year),
                'Month'         :   str(message.created_at.month),
                'Day'           :   str(message.created_at.day),
                'Hour'          :   str(message.created_at.hour),
                'Minute'        :   str(message.created_at.minute),
                'Second'        :   str(message.created_at.second)
            } 
        }

        with open('Data.json', 'w') as jsonFile:
            json.dump(self.data, jsonFile)