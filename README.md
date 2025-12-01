# B2_bot_discord

Bot Discord pédagogique développé en Python dans le cadre du projet B2.  
Il permet d’orienter les utilisateurs vers des métiers de l’informatique, de jouer à un quiz Vrai/Faux et d’obtenir des définitions de notions réseau et programmation.

---

## Objectif du projet

Ce bot a pour but d’aider un utilisateur à :
- Découvrir des métiers de l’informatique selon ses préférences
- Tester ses connaissances avec un jeu Vrai / Faux
- Apprendre les bases du réseau et de la programmation grâce à des définitions

Le projet est entièrement pédagogique.

---

## Prérequis

- Python **3.13.3**
- La bibliothèque **discord.py**
- Un **token de bot Discord**
- Système : Windows

Installation de la librairie :
```bash
pip install discord.py
```

### PARTIE ALARME

## Support vocal (obligatoire pour l'alarme)

Ce bot utilise les fonctionnalités vocales de **:contentReference[oaicite:0]{index=0}**.  
Pour que la commande `/alarme` puisse rejoindre un salon vocal et jouer un son, il faut installer le support audio.

### Installation

Dans le terminal :

```bash
pip install -U "discord.py[voice]"
```

Tu peux remplacer `son.mp3` par **n'importe quel fichier audio de ton choix**, à condition de :

- garder exactement le nom `son.mp3`

Si tu utilises une musique protégée, fais-le uniquement pour un usage **personnel et privé**!

### Emplacement du fichier

Le fichier `son.mp3` doit se trouver dans le même dossier que `main.py`

---

## Dépendance obligatoire : FFmpeg

Ce bot nécessite l'installation de **FFmpeg** pour pouvoir lire les fichiers audio dans les salons vocaux.

Téléchargement :
https://ffmpeg.org

Assure-toi que `ffmpeg.exe` son chemin est bien forcé dans le code via la variable `FFMPEG_PATH`.

MOI SE QUE JE FAIS PERSO C'EST QUE JE DEZIP LE DOSSIER QUE T'INSTALLE VIA (https://ffmpeg.org) ET QUE JE COLLE LE CHEMIN DU FICHIER `\bin\ffmpeg.exe`