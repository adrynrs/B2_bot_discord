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

histo_user: dict[int, CommandHistory] = {}     

class Client(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user}')
    
    async def on_message(self, message):
        if message.author == self.user:
            return
        
        content = message.content.strip()
        user_id = message.author.id

        if user_id not in histo_user:
            histo_user[user_id] = CommandHistory()
        history = histo_user[user_id]

        if content.startswith("/"):
            history.add_command(content)
        
        if content.startswith("/last"):
            last = history.get_last()
            if last is None:
                await message.channel.send("Tu n'as encore envoyé aucune commande.")
            else:
                await message.channel.send(f"Dernière commande enregistrée : `{last}`")

        elif content.startswith("/history"):
            all_commands = history.get_all()
            if not all_commands:
                await message.channel.send("Ton historique est vide.")
            else:
                text = "\n".join(all_commands)
                await message.channel.send(f"Historique des commandes :\n{text}")

        elif content.startswith("/clear_history"):
            history.clear()
            await message.channel.send("Historique Vidé.")



intents = discord.Intents.default()
intents.message_content = True

client = Client(intents=intents)
client.run('') #cle_bot
