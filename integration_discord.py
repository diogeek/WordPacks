import discord
from dotenv import load_dotenv
from replit_keep_alive import keep_alive
import os
import main

load_dotenv("discord_token.env")

iencli = discord.Client()

channels_echanges=[]
suppression = []

prefix = "!"


@iencli.event
async def on_ready():
    print(f'Logged in as {iencli.user.name} - {iencli.user.id}')
    await iencli.change_presence(activity=discord.Game(
        name="!help pour les commandes"))

@iencli.event
async def on_message(message):
    global channels_echanges, suppression
    if message.author.id == iencli.user.id:  #empêcher que le bot ne détecte ses propres messages
        return None

    elif message.content == f"{prefix}help":
        await message.channel.send(f"**Commandes du bot Wordpacks**\n\n\
`{prefix}help` - afficher cette page\n\n\
<a:dresseur:958663675374370836> _Commandes relatives aux dresseurs_\n\n\
`{prefix}kukujariv` - s'inscrire en tant que dresseur.\n\
`{prefix}info` - afficher diverses informations sur votre profil de dresseur.\n\
`{prefix}classement` - afficher le classement des 10 meilleurs dresseurs, ainsi que votre position actuelle.\n\
`{prefix}quitter` - supprimer votre profil de dresseur ainsi que tous vos mots, **définitivement**. Une confirmation vous sera demandée.\n\n\
<a:mokeball:958666482894643200> _Commandes relatives aux mots_\n\n\
`{prefix}mokedex` - afficher les mots que vous possédez, ainsi que leur rareté. Les mots sont triés par rareté.\n\
`{prefix}recherche [mot]` - vérifier si vous possédez un mot.\n\
`{prefix}booster` - ouvrir un booster de 3 mots ! Vous obtenez 3 boosters toutes les 12 heures.\n\
`{prefix}megabooster` - ouvrir 3 boosters de 3 mots, pour 9 mots **SANS DOUBLONS** !\n\
`{prefix}upgrade <nombre>` - sacrifier des boosters (1 de base) pour augmenter la rareté de 2 mots aléatoires de votre mokédex par booster sacrifié.\n\
`{prefix}echange [dresseur]` - proposer un échange avec un dresseur.\n\n\
<:trade:958666805889601576> _Commandes relatives à l'échange_\n\n\
`{prefix}accepter` - accepter la proposition d'échange et créer un channel temporaire.\n\
`{prefix}refuser` - refuser la proposition d'échange.\n\
`{prefix}annuler` - annuler l'échange / la proposition d'échange et supprimer le potentiel channel temporaire.\n\
`{prefix}` - compléter l'échange.")
    if not main.check_dresseur_existe(
            message.author.id) and message.content == f"{prefix}kukujariv":
        main.creer_dresseur(str(message.author.id))
        await message.channel.send(
            f"Dresseur <@{message.author.id}> créé ! Voici **5** boosters pour commencer. Attrapez les tous !"
        )
    elif main.check_dresseur_existe(message.author.id):
        all_echanges=main.dresseur2(message.author.id)
        if all_echanges and message.content == f"{prefix}accepter":
          for echange in all_echanges:
            channel_echange=await message.guild.create_text_channel('echange-temp')
            main.creer_channel_echange(channel_echange.id,echange[1],message.author.id)
            channels_echanges.append(channel_echange.id)
            await message.channel.send(f"Échange entre <@{echange[1]}> et <@{message.author.id}> commencé ! Un channel temporaire a été créé : <#{channel_echange.id}>")
            await channel_echange.send(f"Bienvenue dans un channel temporaire d'échange ! Entrez le mot que vous souhaitez échanger et utilisez tous les deux la commande `{prefix}confirmer` pour compléter l'échange.\n\|| @everyone ||"
            )

        elif main.dresseur2(message.author.id) and message.content == f"{prefix}refuser":
            await message.channel.send("Échange refusé.")

        elif (main.dresseur1(message.author.id) or main.dresseur2(message.author.id)) and message.content == f"{prefix}annuler":
            await message.channel.send("Échange annulé.")
            if message.channel.id in channels_echanges:
              channels_echanges.pop(channels_echanges.index(message.channel.id))
              message.channel.delete()

        elif message.content == f"{prefix}mokedex":
            record = main.afficher_mots(str(message.author.id))
            record = [record[i:i + 50] for i in range(0, len(record), 50)]
            await message.channel.send(
                f"Le dresseur <@{message.author.id}> possède les mots suivants :"
            )
            [await message.channel.send(f"`{(', '.join(x))}`") for x in record]

        elif message.content == f"{prefix}booster":
            if main.boosters_dispo(message.author.id)[0]:
                (record, mots_upgrade), boosters_restants = main.ouverture_booster(
                    message.author.id)
                await message.channel.send(
                    f"""Bravo <@{message.author.id}> ! Tu obtiens les mots suivants : **{(', '.join(record))}**{f" et upgrade les mots suivants : **{(', ').join(mots_upgrade)}**" if mots_upgrade else ""}. Il te reste {boosters_restants} boosters !"""
                )
            else:
                if main.cooldown_ready(message.author.id)[0]:
                    main.remplir_boosters(message.author.id)
                    record = []
                    (record, mots_upgrade), boosters_restants = main.ouverture_booster(
                        message.author.id)
                    await message.channel.send(
                        f"""Bravo <@{message.author.id}> ! Tu obtiens les mots suivants : **{(', '.join(record))}**{f" et upgrade les mots suivants : **{(', ').join(mots_upgrade)}**" if mots_upgrade else ""}. Il te reste {boosters_restants} boosters !"""
                    )
                else:
                    await message.channel.send(
                        f"Désolé <@{message.author.id}>, réessaie dans {main.cooldown_ready(message.author.id)[1]}"
                    )

        elif message.content == f"{prefix}megabooster":
            if main.boosters_dispo(message.author.id, 3)[0]:
                (record, mots_upgrade), boosters_restants = (main.ouverture_booster(
                    message.author.id, 3))
                await message.channel.send(
                    f"""Bravo <@{message.author.id}> ! Tu obtiens les mots suivants : **{(', '.join(record))}**{f" et upgrade les mots suivants : **{(', ').join(mots_upgrade)}**" if mots_upgrade else ""}. Il te reste {boosters_restants} boosters !"""
                )
            else:
                if main.cooldown_ready(message.author.id)[0]:
                    main.remplir_boosters(message.author.id)
                    record = []
                    (record, mots_upgrade), boosters_restants = main.ouverture_booster(
                        message.author.id, 3)
                    await message.channel.send(
                        f"""Bravo <@{message.author.id}> ! Tu obtiens les mots suivants : **{(', '.join(record))}**{f" et upgrade les mots suivants : **{(', ').join(mots_upgrade)}**" if mots_upgrade else ""}. Il te reste {boosters_restants} boosters !"""
                    )
                else:
                    await message.channel.send(
                        f"Désolé <@{message.author.id}>, réessaie dans {main.cooldown_ready(message.author.id)[1]}"
                    )

        elif message.content.startswith(f"{prefix}recherche "):
            if main.check_mot(
                    message.content.split(" ")[1], message.author.id):
                await message.channel.send(
                    f":white_check_mark: Le dresseur <@{message.author.id}> **possède** le mot '{message.content.split(' ')[1]}'."
                )
            else:
                await message.channel.send(
                    f":no_entry_sign: Le dresseur <@{message.author.id}> **ne possède pas** le mot '{message.content.split(' ')[1]}'."
                )

        elif message.content == f"{prefix}jecheat":
            main.remplir_boosters(message.author.id, 999)
            await message.channel.send("Joyeux Anniversaire :)), vous avez obtenu 999 boosters !")
        #elif message.content.startswith(f"{prefix}entrermot "):
        #main.capturer_mots([message.content.split(" ")[1]],message.author.id)
      
        elif message.content.startswith(
                f"{prefix}echange "
        ):
          try:
            if message.mentions[0].id != message.author.id:
              main.proposer_echange(message.author.id,message.mentions[0].id,message.channel.id)
              if main.check_dresseur_existe(message.mentions[0].id):
                  await message.channel.send(
                      f"Le dresseur <@{message.author.id}> propose un **échange** avec le dresseur <@{message.mentions[0].id}> !\n\
  <@{message.mentions[0].id}>, utilisez les commandes `{prefix}accepter` ou `{prefix}refuser`."
                  )
              else:
                  await message.channel.send(
                      f"Dresseur '{message.mentions[0].id}' introuvable.")
          except IndexError:
            await message.channel.send(f"Dresseur '{message.content.split(' ')[1]}' introuvable.")

        elif message.content == f"{prefix}confirmer" and message.channel.id in channels_echanges:
            await message.channel.send(
                f"Le dresseur <@{message.author.id}> confirme l'échange."
            )
            if main.halfcomplete(message.channel.id):
                await iencli.get_channel(main.origine(message.channel.id)).send(main.echanger_mots(message.channel.id))
                channels_echanges.pop(channels_echanges.index(message.channel.id))
                await message.channel.delete()
            else:
                main.confirmer_mot(message.channel.id)

        elif message.channel.id in channels_echanges:
            if not main.check_mot(message.content, message.author.id):
                await message.channel.send(f"Le dresseur <@{message.author.id}> ne possède pas le mot '{message.content}'. Veuillez rééssayer.")
            else:
                main.changer_mot(message.channel.id,message.author.id,message.content)
                await message.channel.send(f"Le dresseur <@{message.author.id}> propose le mot '{message.content}' pour l'échange !")

        elif message.content == f"{prefix}quitter":
            suppression.append(message.author.id)
            await message.channel.send(f"<@{message.author.id}>, entrez `confirmer` pour confirmer la suppression de votre profil de dresseur, ou `annuler` pour annuler la suppression.")

        elif message.content == "confirmer" and message.author.id in suppression:
            suppression.pop(suppression.index(message.author.id))
            await message.channel.send(main.suppression_dresseur(message.author.id))

        elif message.content == "annuler" and message.author.id in suppression:
            suppression.pop(suppression.index(message.author.id))
            await message.channel.send("Suppression annulée. Ouf !")

        elif message.content.startswith("!upgrade"):
            try:
                await message.channel.send(main.upgrade(message.author.id,int(message.content.split(" ")[1])))
            except:
                await message.channel.send(main.upgrade(message.author.id))
        elif message.content == "!info":
            await message.channel.send(main.info(message.author.id, message.author.name))

keep_alive()
iencli.run(os.getenv('TOKEN'))
