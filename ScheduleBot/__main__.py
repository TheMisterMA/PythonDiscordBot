import discord
from scheduleBotClient import ScheduleBotClient
from constants import BOT_TOKEN

client = ScheduleBotClient()
client.run(BOT_TOKEN)