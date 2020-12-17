# Work with Python 3.6
import discord

TOKEN = 'Nzg5MDQ5OTc2MzMxNTY3MTA0.X9saDg.aiFJvOC9li_d28pmxdXwGny9Stk'

client = discord.Client()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)

@client.event
async def on_ready():
    print('-----------------------------------------------------------------')
    print('--\tLogged in as:\t', client.user.name, '\t\n--\tID number:\t', client.user.id)
    print('-----------------------------------------------------------------')

client.run(TOKEN)