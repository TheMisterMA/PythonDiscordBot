# Work with Python 3.6
import discord

TOKEN = 'Nzg5MDQ5OTc2MzMxNTY3MTA0.X9saDg.aiFJvOC9li_d28pmxdXwGny9Stk'

client = discord.Client()

class MyClient(discord.Client):
    async def on_ready(self):
        print('-----------------------------------------------------------------')
        print('--\tLogged in as:\t', self.user.name, '\t\n--\tID number:\t', self.user.id)
        print('-----------------------------------------------------------------')

    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return

        if message.author.id == 175941846650847232:
            print("The author :\t", message.author.name, "\tWith the ID :\t", message.author.id)
            await message.reply('The almighty admin', mention_author=False)

        elif message.content.startswith('- hello'):
            print("The author :\t", message.author.name, "\tWith the ID :\t", message.author.id)
            await message.channel.send('Hello!')

client = MyClient()
client.run(TOKEN)