import discord
from discord.ext import tasks, commands
from scheduleBotClient import ScheduleBotClient
from constants import BOT_TOKEN, MAIN_GUILD_ID

client = ScheduleBotClient()

#@tasks.loop(minutes=1)
#async def called_once_a_day():
#    for channel in client.get_guild(MAIN_GUILD_ID).channels:
#        if (channel.name == 'bot-testing'):
#            message_channel = channel
#
#    print(f"Got channel {message_channel}")
#
#    await message_channel.send("Loop check")
#
#@called_once_a_day.before_loop
#async def before():
#    await client.wait_until_ready()
#    print("Finished waiting")
#
#called_once_a_day.start()

client.run(BOT_TOKEN)