import discord

class Client(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user}')
    
    async def on_message(self, message):
        if message.author == self.user:
            return
        
        if message.content.startswith('/help'):
            await message.channel.send('Hello ')

intents = discord.Intents.default()
intents.message_content = True

client = Client(intents=intents)
client.run('') #cle_bot


