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
<a:dresseur:958663675374370836> _Commandes relatives aux dresseurs_\n\n\
`{prefix}kukujariv` - s'inscrire en tant que dresseur.\n\
`{prefix}info` - afficher votre nombre de points et de boosters disponibles ainsi que votre position dans le classement.\n\
`{prefix}classement` - afficher le classement des 10 dresseurs avec le plus de mots, ainsi que votre position.\n\
`{prefix}quitter` - supprimer votre profil de dresseur ainsi que tous vos mots, **définitivement**. Une confirmation vous sera demandée.\n\n\
<a:mokeball:958666482894643200> _Commandes relatives aux mots_\n\n\
`{prefix}mokedex` - afficher les mots que vous possédez, ainsi que leur rareté. Les mots sont triés par rareté.\n\
`{prefix}recherche [mot]` - vérifier si vous possédez un mot.\n\
`{prefix}booster` - ouvrir un booster de 3 mots ! Vous obtenez 3 boosters toutes les 12 heures.\n\
`{prefix}megabooster` - ouvrir 3 boosters de 3 mots, pour 9 mots **SANS DOUBLONS** !\n\
`{prefix}upgrade` - sacrifier un booster, pour augmenter la rareté de 2 mots aléatoires de votre mokédex.\n\
`{prefix}echange [dresseur]` - proposer un échange avec un dresseur.\n\n\
<:trade:958666805889601576> _Commandes relatives à l'échange_\n\n\
`{prefix}accepter` - accepter la proposition d'échange\n\
`{prefix}refuser` - refuser la proposition d'échange.\n\
`{prefix}annuler` - annuler l'échange.\n\
`{prefix}completer` - compléter l'échange.")
    if not main.check_dresseur_existe(message.author.id) and message.content==f"{prefix}kukujariv":
        main.creer_dresseur(str(message.author.id))
        await message.channel.send(f"Dresseur <@{message.author.id}> créé ! Voici **5** boosters pour commencer. Attrapez les tous !")
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
            record=[record[i:i+50] for i in range(0, len(record), 50)]
            await message.channel.send(f"Le dresseur <@{message.author.id}> possède les mots suivants :")
            [await message.channel.send(f"`{(', '.join(x))}`") for x in record]

        elif message.content==f"{prefix}booster":
          if main.boosters_dispo(message.author.id)[0]:
            record=main.ouverture_booster(message.author.id)
            await message.channel.send(f"Bravo <@{message.author.id}> ! tu obtiens les mots suivants : **{(', '.join(record[0]))}**. Il te reste {record[1]} boosters !")
          else :
            if main.cooldown_ready(message.author.id)[0]:
              main.remplir_boosters(message.author.id)
              record=[]
              record=main.ouverture_booster(message.author.id,3)
              await message.channel.send(f"Bravo <@{message.author.id}> ! tu obtiens les mots suivants : **{(', '.join(record[0]))}**. Il te reste {record[1]} boosters !")
            else :
              await message.channel.send(f"Désolé <@{message.author.id}>, réessaie dans {main.cooldown_ready(message.author.id)[1]}")


        elif message.content.startswith(f"{prefix}recherche "):
          if main.check_mot(message.content.split(" ")[1],message.author.id):
            await message.channel.send(f":white_check_mark: Le dresseur <@{message.author.id}> **possède** le mot '{message.content.split(' ')[1]}'.")
          else:
            await message.channel.send(f":no_entry_sign: Le dresseur <@{message.author.id}> **ne possède pas** le mot '{message.content.split(' ')[1]}'.")
          
        elif message.content==f"{prefix}jecheat":
          main.remplir_boosters(message.author.id,999)
          #await message.channel.send("Joyeux Anniversaire :)), vous avez obtenu 999 boosters !")
        #elif message.content.startswith(f"{prefix}entrermot "):
          #main.capturer_mots([message.content.split(" ")[1]],message.author.id)
      
        elif message.content==f"{prefix}megabooster":
          if main.boosters_dispo(message.author.id,3)[0]:
            record=(main.ouverture_booster(message.author.id,3))
            await message.channel.send(f"Bravo <@{message.author.id}> ! Tu obtiens les mots suivants : **{(', '.join(record[0]))}**. Il te reste {record[1]} boosters !")
          else :
            print(main.cooldown_ready(message.author.id)[1])
            if main.cooldown_ready(message.author.id)[0]:
              main.remplir_boosters(message.author.id)
              record=[]
              record=main.ouverture_booster(message.author.id,3)
              await message.channel.send(f"Bravo <@{message.author.id}> ! tu obtiens les mots suivants : **{(', '.join(record[0]))}**. Il te reste {record[1]} boosters !")
            else: await message.channel.send(f"Désolé <@{message.author.id}>, réessaie dans {main.cooldown_ready(message.author.id)[1]}")

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

        elif message.content.startswith("!upgrade"):
          try: await message.channel.send(main.upgrade(message.author.id,int(message.content.split(" ")[1])))
          except: await message.channel.send(main.upgrade(message.author.id))
        elif message.content=="!info":
          await message.channel.send(main.info(message.author.id,message.author.name))

keep_alive()
iencli.run(os.getenv('TOKEN'))