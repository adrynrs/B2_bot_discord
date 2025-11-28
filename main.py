import discord

class Node:
    def __init__(self, value: str):
        self.value = value
        self.next = None

class CommandHistory:
    def __init__(self):
        self.head = None

    def add_command(self, command: str):
        new_node = Node(command)
        new_node.next = self.head
        self.head = new_node

    def get_last(self):
        if self.head is None:
            return None
        return self.head.value
    
    def get_all(self):
        command = []
        current = self.head
        while current is not None:
            command.append(current.value)
            current = current.next
        command.reverse()
        return command
    
    def clear(self):
        self.head = None

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
