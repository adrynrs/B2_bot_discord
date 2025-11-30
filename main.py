import discord
import json
import os

CHANNEL_ID = 1443981407704584202
HISTORY_FILE = "histo_command.json"

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

def save_history_to_JSON():
    data: dict[str, list[str]] = {}
    for user_id, history in histo_user.items():
        data[str(user_id)] = history.get_all()
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_history_from_JSON():
    if not os.path.exists(HISTORY_FILE):
        return
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            return
    for user_id_str, commands in data.items():
        try:
            user_id = int(user_id_str)
        except ValueError:
            continue
        history = CommandHistory()
        for command in commands:
            history.add_command(command)
        histo_user[user_id] = history    

class TreeNode:
    def __init__(self, text: str, is_leaf: bool = False):
        self.text = text
        self.is_leaf = is_leaf
        self.children: dict[str, "TreeNode"] = {}

user_positions: dict[int, TreeNode] = {}

dev_frontend = TreeNode(
    "Conclusion : tu préfères le développement frontend. "
    "Regarde les métiers de développeur frontend, intégrateur, ou UI engineer.\n"
    "Refait `/help` pour refaire ou `/show` pour voir les commandes disponibles.",
    is_leaf=True,
)

dev_backend = TreeNode(
    "Conclusion : tu préfères le développement backend. "
    "Regarde les métiers de développeur backend, API engineer ou architecte logiciel.\n"
    "Refait `/help` pour refaire ou `/show` pour voir les commandes disponibles.",
    is_leaf=True,
)

data_analyst = TreeNode(
    "Conclusion : tu sembles intéressé par l'analyse de données. "
    "Regarde les métiers de data analyst, BI, reporting.\n"
    "Refait `/help` pour refaire ou `/show` pour voir les commandes disponibles.",
    is_leaf=True,
)

data_scientist = TreeNode(
    "Conclusion : tu sembles intéressé par la data science / IA. "
    "Regarde les métiers de data scientist, machine learning engineer.\n"
    "Refait `/help` pour refaire ou `/show` pour voir les commandes disponibles.",
    is_leaf=True,
)

q2_dev = TreeNode(
    "Tu préfères :\n"
    "1 - Frontend (interfaces, UI)\n"
    "2 - Backend (serveurs, APIs)\n"
    "répond que par `1` ou `2`"
)
q2_dev.children["1"] = dev_frontend
q2_dev.children["2"] = dev_backend

q2_data = TreeNode(
    "Tu préfères :\n"
    "1 - Analyser / visualiser les données\n"
    "2 - Construire des modèles d'IA / machine learning\n"
    "répond que par `1`, `2`"
)
q2_data.children["1"] = data_analyst
q2_data.children["2"] = data_scientist

reseau_admin = TreeNode(
    "Conclusion : tu préfères l'administration réseau / infrastructure. "
    "Regarde les métiers d'administrateur réseau, ingénieur cloud, ou sysadmin.\n"
    "Refait `/help` pour refaire ou `/show` pour voir les commandes disponibles.",
    is_leaf=True,
)

reseau_secu = TreeNode(
    "Conclusion : tu préfères la sécurité / cybersécurité. "
    "Regarde les métiers d'analyste SOC, pentester ou ingénieur sécurité.\n"
    "Refait `/help` pour refaire ou `/show` pour voir les commandes disponibles.",
    is_leaf=True,
)

q2_reseau = TreeNode(
    "Tu préfères :\n"
    "1 - Administration réseau / infra\n"
    "2 - Sécurité / cybersécurité\n"
    "répond que par `1` ou `2`"
)
q2_reseau.children["1"] = reseau_admin
q2_reseau.children["2"] = reseau_secu

root_node = TreeNode(
    "Orientation pro - Tu préfères bosser dans le monde du:\n"
    "1 - dev\n"
    "2 - réseau\n"
    "3 - data\n"
    "répond que par `1`, `2` ou `3`"
)
root_node.children["1"] = q2_dev
root_node.children["2"] = q2_reseau
root_node.children["3"] = q2_data

def speak_about_X(node: TreeNode, subject: str) -> bool:
    subject = subject.lower()
    if subject in node.text.lower():
        return True
    for child in node.children.values():
        if speak_about_X(child, subject):
            return True
    return False

class GameState:
    def __init__(self):
        self.quest = 0
        self.score = 0

user_games: dict[int, GameState] = {}

GAME_QUESTIONS = [
    (
        "HTML est un langage de programmation ?\n"
        "Repond par `vrai` ou `faux`.",
        False,
        "HTML est un langage de balisage."
    ),
    (
        "la couche 4 du modele osi est appeler couche transport ?\n"
        "Repond par `vrai` ou `faux`.",
        True,
        "La couche 4 est bien la couche transport (ex : TCP/UDP)."
    ),
    (
        "est-ce qu'un anti-virus permet d'être plus discret sur internet ?\n"
        "Repond par `vrai` ou `faux`.",
        False,
        "Un anti-virus protege contre les malwares, mais n'assure pas l'anonymat."
    ),
    (
        "Python est un langage interpreté ?\n"
        "Repond par `vrai` ou `faux`.",
        True,
        "Python est généralement interprété."
    ),
    (
        "Le routeur sert uniquement à se connecter au Wi-Fi ?\n"
        "Repond par `vrai` ou `faux`.",
        False,
        "Un routeur fait bien plus, ce n'est pas sa seule fonction."
    ),
]

class Client(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user}')
        load_history_from_JSON()

        channel = self.get_channel(CHANNEL_ID)
        if channel is not None:
            await channel.send("Pour voir les commandes disponibles, tape `/show`.")
    
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
            save_history_to_JSON()

        if content.startswith('/show'):
            await message.channel.send(
                "`/help` : QCM orientation pro\n"
                "`/game` : lance un jeu Vrai/Faux sur l'informatique.\n"
                "`/last` : affiche la dernière commande que tu as envoyée.\n"
                "`/history` : affiche toutes tes commandes enregistrées (du plus ancien au plus récent).\n"
                "`/clear_history` : efface ton historique de commandes.\n"
                "`speak about X` : vérifie si le sujet X existe dans l'arbre.\n"
            )

            if user_id in user_positions:
                current_node = user_positions[user_id]
                await message.channel.send(
                "TU N'AS PAS FINI LE QUESTIONNAIRE:\n"
                    + current_node.text
                )
            return
        
        elif content.startswith('/game'):
            user_games[user_id] = GameState()
            game_state = user_games[user_id]
            question, _, _ = GAME_QUESTIONS[game_state.quest]
            await message.channel.send(
                "Jeu Vrai/Faux lancé ! Réponds uniquement par `vrai` ou `faux`.\n\n"
                f"Question 1/{len(GAME_QUESTIONS)} :\n{question}"
            )
            return

        elif content.startswith('/help'):
            user_positions[user_id] = root_node
            await message.channel.send(root_node.text)
            return
        
        elif content.startswith('/reset'):
            user_positions[user_id] = root_node
            await message.channel.send("On recommence :\n" + root_node.text)
            return
        
        elif content.lower().startswith('speak about '):
            subject = content[len('speak about '):].strip()
            if speak_about_X(root_node, subject):
                await message.channel.send("oui")
            else:
                await message.channel.send("non")
            return
        
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
            save_history_to_JSON()
            await message.channel.send("Historique clear")

        if not content.startswith("/") and user_id in user_games:
            state = user_games[user_id]
            answer = content.lower()

            if answer not in ("vrai", "faux"):
                await message.channel.send("Réponds seulement par `vrai` ou `faux`.")
                return
            
            question_text, correct_answer, explanation = GAME_QUESTIONS[state.quest]
            user_is_true = (answer == "vrai")

            if user_is_true == correct_answer:
                state.score += 1
                await message.channel.send("Bonne réponse !")
            else:
                await message.channel.send("Mauvaise réponse.")
            await message.channel.send(explanation)

            state.quest += 1

            if state.quest >= len(GAME_QUESTIONS):
                await message.channel.send(
                    f"Jeu terminé ! Ton score : {state.score}/{len(GAME_QUESTIONS)}.\n"
                    "Tape `/game` pour rejouer ou `/show` pour voir les commandes disponibles."
                )
                del user_games[user_id]

            else:
                next_question, _, _ = GAME_QUESTIONS[state.quest]
                await message.channel.send(
                    f"Question {state.quest + 1}/{len(GAME_QUESTIONS)} :\n{next_question}"
                )
            return
        

        
        if not content.startswith("/") and user_id in user_positions:
            current_node = user_positions[user_id]
            choice = content
            if choice in current_node.children:
                next_node = current_node.children[choice]
                user_positions[user_id] = next_node

                if next_node.is_leaf:
                    await message.channel.send(next_node.text)
                    del user_positions[user_id]
                else:
                    await message.channel.send(next_node.text)
            else:
                await message.channel.send(
                    "Je n'ai pas compris ta réponse."
                    f"Tu dois choisir parmi : {', '.join(current_node.children.keys())}"
                )

intents = discord.Intents.default()
intents.message_content = True

client = Client(intents=intents)
client.run('') #cle_bot
