import discord
from dotenv import load_dotenv
from keep_alive import keep_alive
import os
import main

load_dotenv("discord_token.env")

iencli = discord.Client()

trade_en_cours=False
proposition_trade=False
dresseur1_trade=""
dresseur2_trade=""
dresseur1_mot=""
dresseur2_mot=""
half_complete=False
suppression=""

prefix="!"

@iencli.event
async def on_ready():
    print(f'Logged in as {iencli.user.name} - {iencli.user.id}')
    await iencli.change_presence(activity=discord.Game(name="!help pour les commandes"))

@iencli.event
async def on_message(message):
    global trade_en_cours,proposition_trade,dresseur1_trade,dresseur2_trade,dresseur1_mot,dresseur2_mot,half_complete,suppression
    if message.author.id == iencli.user.id :#empêcher que le bot ne détecte ses propres messages
        return None

    elif message.content==f"{prefix}help":
        await message.channel.send(f"**Commandes du bot Wordpacks**\n\n\
`{prefix}help` - afficher cette page\n\n\
_Commandes principales_\n\n\
`{prefix}kukujariv` - s'inscrire en tant que dresseur\n\
`{prefix}mokedex` - afficher les mots que vous possédez\n\
`{prefix}booster` - ouvrir un booster de 3 mots\n\
`{prefix}quitter` - supprimer votre profil de dresseur ainsi que tous vos mots, **définitivement**. Une confirmation est obligatoire\n\
`{prefix}echange [dresseur]` - proposer un échange avec un dresseur\n\n\
_Commandes relatives à l'échange_\n\n\
`{prefix}accepter` - accepter la proposition d'échange\n\
`{prefix}refuser` - refuser la proposition d'échange\n\
`{prefix}annuler` - annuler l'échange\n\
`{prefix}completer` - compléter l'échange")
    if not main.check_dresseur_existe(message.author.id) and message.content==f"{prefix}kukujariv":
        main.creer_dresseur(str(message.author.id))
        await message.channel.send(f"Dresseur <@{message.author.id}> créé ! Attrapez les tous !")
    elif main.check_dresseur_existe(message.author.id):
        if proposition_trade and message.author.id==dresseur2_trade and message.content==f"{prefix}accepter":
            proposition_trade=False
            trade_en_cours=True
            await message.channel.send(f"Échange entre <@{dresseur1_trade}> et <@{dresseur2_trade}> commencé !\n\
entrez le mot que vous souhaitez échanger et utilisez tous les deux la commande `{prefix}completer` pour compléter.")

        elif proposition_trade and message.author.id==dresseur2_trade and message.content==f"{prefix}refuser":
            proposition_trade=False
            await message.channel.send("Échange refusé.")

        elif ((trade_en_cours and message.author.id in [dresseur2_trade,dresseur1_trade]) or (proposition_trade and message.author.id==dresseur1_trade)) and message.content==f"{prefix}annuler":
            trade_en_cours=False
            await message.channel.send("Échange annulé.")
          
        elif message.content==f"{prefix}mokedex":
            record=main.afficher_mots(str(message.author.id))
            await message.channel.send(f"Le dresseur <@{message.author.id}> possède les mots suivants : **{(', '.join([raw[0] for raw in record]))}**")

        elif message.content==f"{prefix}booster":
          if main.cooldown_ready(message.author.id)[0]:
            record=main.ouverture_booster(message.author.id)
            await message.channel.send(f"Bravo <@{message.author.id}> ! tu obtiens les mots suivants : **{(', '.join(record))}**")
          else :
            await message.channel.send(f"Désolé <@{message.author.id}>, réessaie dans {main.cooldown_ready(message.author.id)[0]}")

        elif message.content.startswith(f"{prefix}echange ") and message.mentions[0].id!=message.author.id:
            dresseur1_trade=message.author.id
            dresseur2_trade=message.mentions[0].id
            if main.check_dresseur_existe(dresseur2_trade):
              proposition_trade=True
              await message.channel.send(f"Le dresseur <@{dresseur1_trade}> propose un **échange** avec le dresseur <@{dresseur2_trade}> ! \
<@{dresseur2_trade}>, utilisez les commandes `{prefix}accepter` ou `{prefix}refuser`.")
            else : await message.channel.send(f"Dresseur '{dresseur2_trade}' introuvable.")
    
        elif trade_en_cours and message.author.id in [dresseur1_trade,dresseur2_trade] and [dresseur1_mot,dresseur2_mot][[dresseur1_trade,dresseur2_trade].index(message.author.id)]!="" and message.content==f"{prefix}completer":
            await message.channel.send(f"Le dresseur <@{message.author.id}> bloque le mot '{[dresseur1_mot,dresseur2_mot][[dresseur1_trade,dresseur2_trade].index(message.author.id)]}'.")
            if half_complete:
                await message.channel.send(main.echanger_mots(dresseur1_mot,dresseur2_mot,dresseur1_trade,dresseur2_trade))
            else : half_complete=True

        elif trade_en_cours and message.author.id in [dresseur1_trade,dresseur2_trade]:
            if main.check_mot(message.content,message.author.id)=="":
                await message.channel.send(f"Le dresseur <@{message.author.id}> ne possède pas le mot '{message.content}'. Veuillez rééssayer.")
            else :
              if message.author.id==dresseur1_trade: dresseur1_mot=message.content
              else: dresseur2_mot=message.content
              await message.channel.send(f"Le dresseur <@{message.author.id}> propose le mot '{message.content}' pour l'échange !")
          
        elif message.content==f"{prefix}quitter":
          suppression=message.author.id
          await message.channel.send(f"<@{message.author.id}>, entrez `confirmer` pour confirmer la suppression de votre profil de dresseur, ou `annuler` pour annuler la suppression.")
      
        elif message.content=="confirmer" and message.author.id==suppression:
            await message.channel.send(main.suppression_dresseur(message.author.id))
      
        elif message.content=="annuler" and message.author.id==suppression:
          suppression=""
          await message.channel.send("Suppression annulée. Ouf !")

keep_alive()
iencli.run(os.getenv('TOKEN'))
