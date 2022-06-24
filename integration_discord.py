import discord
from dotenv import load_dotenv
from replit_keep_alive import keep_alive
import os
import main

load_dotenv("discord_token.env")

iencli = discord.Client()

numbers=[":one:",":two:",":three:",":four:",":five:",":six:",":seven:",":eight:",":nine:",":keycap_ten:"]

dio=0
@iencli.event
async def on_ready():
  global dio
  dio=await iencli.fetch_user(504697143932485656)
  for server in iencli.guilds:
    main.ajouter_serveur(server.id)
  print(f'Logged in as {iencli.user.name} - {iencli.user.id}')
  await iencli.change_presence(activity=discord.Game(name="!intro / !help"))

@iencli.event
async def on_message(message):
    if message.author.id == iencli.user.id:  #empêcher que le bot ne détecte ses propres messages
        return None
    elif message.content == f"{main.get_prefix(message.guild.id)}intro":
        await message.channel.send(f"<a:mokeball:958666482894643200> _**WORDPACKS**_ <a:mokeball:958666482894643200>\n\n\
**BIENVENUE** dans la merveilleuse aventure de Wordpacks !\n\
Ceci est l'introduction explicative du bot. Si vous cherchez les commandes, référez vous à `{main.get_prefix(message.guild.id)}help` !\n\n\
Wordpacks est un jeu sous forme de bot.\n\
Le but du jeu est de collectionner des mots de la langue française en les obtenant dans des **boosters**, des petits packs de 3 mots que vous obtiendrez par intervalles de 12 heures.\n\n\
__**Points**__\n\
Lorsqu'un utilisateur de discord écrira l'un de vos mots dans un message, vous obtiendrez un petit nombre de points, égal à la rareté du mot en question.\n\n\
__**Rareté**__\n\
Chacun de vos mots est de rareté 1 de base. Il vous rapportera donc 1 point à chaque utilisation de celui-ci par un utilisateur de Discord. Afin d'augmenter la rareté de l'un de vos mots (jusqu'au maximum de 6), il vous faudra obtenir ce mot autant de fois que son niveau actuel.\n\
Par exemple, pour passer du niveau 4 au niveau 5, il vous faudra obtenir ce mot 4 fois !")
        await message.channel.send("Il vous faudra donc obtenir un mot 15 fois pour le monter au niveau maximum.\n\n\
__**Upgrade**__\n\
Il est aussi possible à l'aide d'une commande de sacrifier l'un de vos boosters disponibles pour obtenir 2 mots que vous avez déjà ! de cette façon vous vous assurez de monter en niveau certains de vos mots, mais ils seront tout de même sélectionnés au hasard dans votre Mokédex.\n\n\
__**Échange**__\n\
Il est possible, à travers certaines commandes, d'échanger un de vos mots avec un mot d'un autre dresseur, dans un salon d'échange privé. ATTENTION ! Chaque mot affecté par l'échange prendra pour rareté la plus basse de celles des mots échangés.\n\
Par exemple, si vous échangez un mot du niveau 4 et un mot du niveau 2, les deux mots seront de niveau 2. de plus, ils perdront d'éventuels mots obtenus pour leur montée de niveau.\n\n\
__**Informations supplémentaires**__\n\
 - Il est parfaitement possible d'obtenir un mot déjà possédé par un dresseur. Le cas échéant, vous lui volerez son mot sans scrupules et sa rareté retombera à 1.\n\
 - Le bot est sûrement rempli de bugs. Si vous en croisez un, mettez un masque et merci d'en parler à <@504697143932485656>, son créateur ! <a:dresseur:958663675374370836>\n\n\
Allez, il ne vous reste plus qu'à utiliser la commande `!kukujariv` pour débuter votre aventure de dresseur Wordpacks !")
    elif message.content == f"{main.get_prefix(message.guild.id)}help":
        await message.channel.send(f"**Commandes du bot Wordpacks**\n\n\
`{main.get_prefix(message.guild.id)}intro` - Wordpacks c'est quoi ?\n\
`{main.get_prefix(message.guild.id)}help` - afficher cette page\n\
`{main.get_prefix(message.guild.id)}wordpacksprefix` [prefix] - changer le prefix des commandes du bot WordPacks (`!` par défaut). Cette commande fonctionnera toujours avec `!wordpacksprefix` afin de pouvoir corriger d'éventuels changements accidentels. La taille maximale d'un prefix est de 5 caractères.\n\n\
<a:dresseur:958663675374370836> _Commandes relatives aux dresseurs_\n\n\
`{main.get_prefix(message.guild.id)}kukujariv` / `{main.get_prefix(message.guild.id)}inscription` - s'inscrire en tant que dresseur.\n\
`{main.get_prefix(message.guild.id)}info <dresseur>` - afficher diverses informations sur votre profil de dresseur. Il est possible d'afficher la carte d'infos d'un autre dresseur en le mentionnant.\n\
`{main.get_prefix(message.guild.id)}classement` - afficher le classement des 10 meilleurs dresseurs, ainsi que votre position actuelle.\n\
`{main.get_prefix(message.guild.id)}quitter` - supprimer votre profil de dresseur ainsi que tous vos mots, **définitivement**. Une confirmation vous sera demandée.\n\n\
<a:mokeball:958666482894643200> _Commandes relatives aux mots_\n\n\
`{main.get_prefix(message.guild.id)}mokedex <dresseur>` - afficher les mots que vous possédez, ainsi que leur rareté. Les mots sont triés par rareté. Il est possible d'afficher le mokédex d'un autre dresseur en le mentionnant.\n\
`{main.get_prefix(message.guild.id)}existe [mot]` / `{main.get_prefix(message.guild.id)}peutonpaké [mot]`- vérifier si un mot est obtenable dans un booster.\n\
`{main.get_prefix(message.guild.id)}recherche [mot] <dresseur>` - vérifier si vous possédez un mot. Il est possible de faire une recherche dans le mokédex d'un autre dresseur en le mentionnant.\n\
`{main.get_prefix(message.guild.id)}booster` - ouvrir un booster de 3 mots ! Vous obtenez 3 boosters toutes les 12 heures.\n\
`{main.get_prefix(message.guild.id)}megabooster` - ouvrir 3 boosters de 3 mots, pour 9 mots **SANS DOUBLONS** !\n\
`{main.get_prefix(message.guild.id)}upgrade <nombre>` - sacrifier des boosters (1 de base) pour augmenter la rareté de 2 mots aléatoires de votre mokédex par booster sacrifié.")
        await message.channel.send(f"`{main.get_prefix(message.guild.id)}echange [dresseur]` - proposer un échange avec un dresseur.\n\n\
<:trade:958666805889601576> _Commandes relatives à l'échange_\n\n\
`{main.get_prefix(message.guild.id)}echangetoggle` - activer/désactiver la possibilité pour les dresseurs de vous proposer des échanges.\n\
`{main.get_prefix(message.guild.id)}accepter <dresseur>` - accepter la proposition d'échange d'un dresseur et créer un channel d'échange temporaire.\n\
`{main.get_prefix(message.guild.id)}acceptertout` - accepter **toutes** les propositions d'échange et créer un channel d'échange temporaire pour chacune d'entre elles.\n\
`{main.get_prefix(message.guild.id)}refuser <dresseur>`  - refuser la proposition d'échange d'un dresseur.\n\
`{main.get_prefix(message.guild.id)}refusertout` - refuser **toutes** les propositions d'échange que l'on vous a fait.\n\
`{main.get_prefix(message.guild.id)}annuler <dresseur>` (en dehors d'un channel d'échange) - annuler la proposition d'échange faite à un dresseur.\n\
`{main.get_prefix(message.guild.id)}annuler` (dans un channel d'échange) - annuler l'échange en cours et supprimer le channel temporaire.\n\
`{main.get_prefix(message.guild.id)}annulertout` - annuler toutes les propositions d'échange que vous avez faites. Ceci n'annulera pas d'éventuels échanges en cours.\n\
`{main.get_prefix(message.guild.id)}confirmer` (dans un channel d'échange) - compléter l'échange.\n\n\
:computer: _Commandes diverses_\n\n\
`{main.get_prefix(message.guild.id)}listemots` - afficher la liste des mots obtenables dans un booster.")
    elif message.content=="!wordpacksaddserver":
      main.ajouter_serveur(message.guild.id)
    elif message.content.startswith("!wordpacksprefix ") or message.content.startswith(f"{main.get_prefix(message.guild.id)}wordpacksprefix "):
      if message.mentions:
        await message.channel.send("Veuillez entrer un prefix valide.")
      elif len(message.content.split(" ")[1])<5:
        try:
          await message.channel.send(main.changer_prefix(message.guild.id,message.content.split(" ")[1]))
        except IndexError:
          await message.channel.send(f"Veuillez entrez un prefix valide.")
    elif not main.check_dresseur_existe(message.author.id,message.guild.id) and (message.content == f"{main.get_prefix(message.guild.id)}kukujariv" or message.content == f"{main.get_prefix(message.guild.id)}inscription"):
        main.creer_dresseur(str(message.author.id),message.guild.id)
        await message.channel.send(
            f"Dresseur <@{message.author.id}> créé ! Voici **5** boosters pour commencer. Utilisez `{main.get_prefix(message.guild.id)}booster` pour en ouvrir un ou `{main.get_prefix(message.guild.id)}help` pour afficher toutes les commandes ! Attrapez les tous !"
        )
    elif message.content == (f"{main.get_prefix(message.guild.id)}listemots"):
        await message.channel.send("**Voici la liste des mots disponibles dans les packs :**", file=discord.File('list_fr.txt','liste_des_mots_disponibles.txt'))
    elif main.check_dresseur_existe(message.author.id,message.guild.id):
        if message.content.startswith(f"{main.get_prefix(message.guild.id)}accepter ") and not main.check_channels_echanges(message.guild.id,message.channel.id) and message.mentions: #accepter la demande en mentionnant qqn
          if main.check_dresseur_existe(message.mentions[0].id,message.guild.id):
            channel_echange=await message.guild.create_text_channel(f'echange-temp-{message.author.name}-{message.mentions[0].name}', overwrites={message.guild.default_role: discord.PermissionOverwrite(read_messages=False),dio: discord.PermissionOverwrite(manage_channels=True),message.author: discord.PermissionOverwrite(read_messages=True),message.mentions[0]: discord.PermissionOverwrite(read_messages=True),iencli.user: discord.PermissionOverwrite(read_messages=True,manage_channels=True)}, category=message.channel.category)
            main.creer_channel_echange(channel_echange.id,message.mentions[0].id,message.author.id,message.guild.id)
            await message.channel.send(f"Échange entre <@{message.mentions[0].id}> et <@{message.author.id}> commencé ! Un channel temporaire a été créé. Pour y accéder, cliquez ici : <#{channel_echange.id}>")
            await channel_echange.send(f"Bienvenue dans un channel temporaire d'échange ! Entrez le mot que vous souhaitez échanger et utilisez tous les deux la commande `{main.get_prefix(message.guild.id)}confirmer` pour compléter l'échange, ou utilisez `{main.get_prefix(message.guild.id)}annuler` à tout moment pour annuler l'échange.\n||@everyone||")
        elif message.content == f"{main.get_prefix(message.guild.id)}acceptertout" and not main.check_channels_echanges(message.channel.id): #accepter toutes les demandes
          all_echanges=main.dresseur2(message.author.id,message.guild.id)
          if all_echanges:
            for echange in all_echanges:
              dresseur2=await iencli.fetch_user(int(echange[2]))
              channel_echange=await message.guild.create_text_channel(f'echange-temp-{message.author.name}-{dresseur2.name}', overwrites={message.guild.default_role: discord.PermissionOverwrite(read_messages=False),dio: discord.PermissionOverwrite(manage_channels=True),message.author: discord.PermissionOverwrite(read_messages=True),dresseur2: discord.PermissionOverwrite(read_messages=True),iencli.user: discord.PermissionOverwrite(read_messages=True,manage_channels=True)}, category=message.channel.category)
              main.creer_channel_echange(channel_echange.id,echange[2],message.author.id,message.guild.id)
              await message.channel.send(f"Échange entre <@{echange[2]}> et <@{message.author.id}> commencé ! Un channel temporaire a été créé. Pour y accéder, cliquez ici : <#{channel_echange.id}>")
              await channel_echange.send(f"Bienvenue dans un channel temporaire d'échange ! Entrez le mot que vous souhaitez échanger et utilisez tous les deux la commande `{main.get_prefix(message.guild.id)}confirmer` pour compléter l'échange, ou utilisez `{main.get_prefix(message.guild.id)}annuler` à tout moment pour annuler l'échange.\n||@everyone||")

        elif main.dresseur2(message.author.id,message.guild.id) and message.content == f"{main.get_prefix(message.guild.id)}refusertout" and not main.check_channels_echanges(message.channel.id): #refuser toutes les demandes
            main.delete_all_echanges(message.author.id,2)
            await message.channel.send("Propositions d'échange refusées.")

        elif main.dresseur2(message.author.id,message.guild.id) and message.content.startswith(f"{main.get_prefix(message.guild.id)}refuser ") and message.mentions and not main.check_channels_echanges(message.guild.id,message.channel.id): #refuser en mentionnant qqn
          if main.check_dresseur_existe(message.mentions[0].id,message.guild.id):
            main.delete_channel_echange(dresseur1=message.mentions[0].id,dresseur2=message.author.id)
            await message.channel.send("Échange refusé.")
            
        elif main.check_channels_echanges(message.guild.id,message.channel.id) and message.content == f"{main.get_prefix(message.guild.id)}annuler": #annuler dans un channel échange
            await message.channel.send("Échange annulé.")
            if main.check_channels_echanges(message.guild.id,message.channel.id):
              main.delete_channel_echange(message.channel.id)
              await message.channel.delete()
              
        elif main.dresseur1(message.author.id,message.guild.id,True) and not main.check_channels_echanges(message.guild.id,message.channel.id) and message.content.startswith(f"{main.get_prefix(message.guild.id)}annuler ") and message.mentions: #annuler la proposition en mentionnant qqn
          if main.check_channels_echanges(message.guild.id,dresseur1=message.author.id,dresseur2=message.mentions[0].id):
            await message.channel.send(f"Échange annulé.\n||<@{message.author.id}>||")
            main.delete_channel_echange(dresseur1=message.author.id,dresseur2=message.mentions[0].id)
              
        elif (main.dresseur1(message.author.id,message.guild.id) or (main.dresseur2(message.author.id,message.guild.id,False) and main.check_channels_echanges(message.guild.id,message.channel.id))) and message.content == f"{main.get_prefix(message.guild.id)}annulertout": #annuler toutes les propositions
            await message.channel.send(f"Échanges annulés.\n||<@{message.author.id}>||")
            main.delete_all_echanges(message.author.id,True) #True : ne supprime que les propositions, pas les échanges en cours

        elif message.content == f"{main.get_prefix(message.guild.id)}echangetoggle":
          await message.channel.send(main.echangetoggle(message.author.id,message.guild.id))
        
        elif message.content.startswith(f"{main.get_prefix(message.guild.id)}mokedex"):
          if not message.mentions:
            record,count = main.afficher_mots(str(message.author.id),message.guild.id)
            record = [record[i:i + 50] for i in range(0, len(record), 50)]
            await message.channel.send(
                f"Le dresseur <@{message.author.id}> possède **{count}** mots :"
            )
            [await message.channel.send(f"{(', '.join(x))} ||<@{message.author.id}>||") for x in record]
          elif main.check_dresseur_existe(message.mentions[0].id,message.guild.id):
            record,count = main.afficher_mots(str(message.mentions[0].id),message.guild.id)
            record = [record[i:i + 50] for i in range(0, len(record), 50)]
            await message.channel.send(
                f"Le dresseur <@{message.mentions[0].id}> possède **{count}** mots :"
            )
            [await message.channel.send(f"`{(', '.join(x))}`") for x in record]
          else :
            await message.channel.send(f"Dresseur `{message.mentions[0].name}` introuvable.")

        elif message.content == f"{main.get_prefix(message.guild.id)}booster":
            if main.boosters_dispo(message.author.id,message.guild.id)[0]:
                (record, mots_upgrade), boosters_restants = main.ouverture_booster(
                    message.author.id,message.guild.id)
                await message.channel.send(
                    f"""Bravo <@{message.author.id}> ! Tu obtiens les mots suivants : **{(', '.join(record))}**{f" et upgrade les mots suivants : **{(', ').join(mots_upgrade)}**" if mots_upgrade else ""}. Il te reste {boosters_restants} boosters !""")
            else:
                if main.cooldown_ready(message.author.id,message.guild.id)[0]:
                    main.remplir_boosters(message.author.id,message.guild.id)
                    record = []
                    (record, mots_upgrade), boosters_restants = main.ouverture_booster(
                        message.author.id,message.guild.id)
                    await message.channel.send(
                        f"""Bravo <@{message.author.id}> ! Tu obtiens les mots suivants : **{(', '.join(record))}**{f" et upgrade les mots suivants : **{(', ').join(mots_upgrade)}**" if mots_upgrade else ""}. Il te reste {boosters_restants} boosters !""")
                else:
                    await message.channel.send(
                        f"Désolé <@{message.author.id}>, réessaie dans {main.cooldown_ready(message.author.id,message.guild.id)[1]}"
                    )

        elif message.content == f"{main.get_prefix(message.guild.id)}megabooster":
            if main.boosters_dispo(message.author.id,message.guild.id, 3)[0]:
                (record, mots_upgrade), boosters_restants = (main.ouverture_booster(
                    message.author.id,message.guild.id, 3))
                await message.channel.send(f"""Bravo <@{message.author.id}> ! Tu obtiens les mots suivants : **{(', '.join(record))}**{f" et upgrade les mots suivants : **{(', ').join(mots_upgrade)}**" if mots_upgrade else ""}. Il te reste {boosters_restants} boosters !""")
            else:
                if main.cooldown_ready(message.author.id,message.guild.id)[0]:
                    main.remplir_boosters(message.author.id,message.guild.id)
                    record = []
                    (record, mots_upgrade), boosters_restants = main.ouverture_booster(
                        message.author.id,message.guild.id, 3)
                    await message.channel.send(f"""Bravo <@{message.author.id}> ! Tu obtiens les mots suivants : **{(', '.join(record))}**{f" et upgrade les mots suivants : **{(', ').join(mots_upgrade)}**" if mots_upgrade else ""}. Il te reste {boosters_restants} boosters !""")
                else:
                    await message.channel.send(f"Désolé <@{message.author.id}>, réessaie dans {main.cooldown_ready(message.author.id,message.guild.id)[1]}")

        elif message.content.startswith(f"{main.get_prefix(message.guild.id)}recherche "):
            dresseur=message.author
            if message.mentions:
              dresseur=message.mentions[0]
            mot=main.check_mot(message.content.split(" ")[1], dresseur.id, message.guild.id)
            if mot:
                await message.channel.send(f":white_check_mark: Le dresseur `{dresseur.name}` **possède** le mot `{mot[0]}`. Sa rareté est de **{mot[1]}** ({mot[1]-mot[2]}/{mot[1]}).\n||<@{message.author.id}>||")
            else:
                await message.channel.send(f":no_entry_sign: Le dresseur `{dresseur.name}` **ne possède pas** le mot '{message.content.split(' ',2)[1]}'.\n||<@{message.author.id}>||")

        #cheats :
        #elif message.content == f"{main.get_prefix(message.guild.id)}jecheat":
            #main.remplir_boosters(message.author.id, 999)
            #await message.channel.send("Joyeux Anniversaire :)), vous avez obtenu 999 boosters !")
        #elif message.content.startswith(f"{main.get_prefix(message.guild.id)}entrermot "):
        #main.capturer_mots([message.content.split(" ")[1]],message.author.id)
      
        elif message.content.startswith(f"{main.get_prefix(message.guild.id)}echange "):
          try:
            if message.mentions[0].id != message.author.id and not main.check_channels_echanges(message.guild.id,dresseur1=message.author.id,dresseur2=message.mentions[0].id) and not main.check_channels_echanges(message.guild.id,dresseur1=message.mentions[0].id,dresseur2=message.author.id):
              if main.check_dresseur_existe(message.mentions[0].id,message.guild.id):
                if main.check_echange_ouvert(message.mentions[0].id,message.guild.id):
                  main.proposer_echange(message.author.id,message.mentions[0].id,message.guild.id,message.channel.id)
                  await message.channel.send(
                      f"Le dresseur <@{message.author.id}> propose un **échange** avec le dresseur <@{message.mentions[0].id}> !\n\
  <@{message.mentions[0].id}>, utilisez les commandes `{main.get_prefix(message.guild.id)}accepter @{message.author.name}` ou `{main.get_prefix(message.guild.id)}refuser @{message.author.name}`. <@{message.author.id}>, utilisez la commande `{main.get_prefix(message.guild.id)}annuler @{message.mentions[0].name}` à tout moment pour annuler cette proposition d'échange, ou `{main.get_prefix(message.guild.id)}annulertout` pour annuler toutes vos propositions d'échange en cours."
                  )
                else:
                  await message.channel.send(f"Désolé <@{message.author.id}>, ce dresseur n'accepte pas les propositions d'échange.")
              else:
                  await message.channel.send(
                      f"Dresseur `{message.mentions[0].name}` introuvable.\n||<@{message.author.id}>||")
          except IndexError:
            await message.channel.send(f"Dresseur '{message.content.split(' ')[1]}' introuvable.")

        elif message.content == f"{main.get_prefix(message.guild.id)}confirmer" and main.check_channels_echanges(message.guild.id,message.channel.id):
          if main.mot_propose(message.author.id,message.channel.id):
            await message.channel.send(
                f"Le dresseur <@{message.author.id}> confirme l'échange."
            )
            if main.halfcomplete(message.channel.id):
                channel=await iencli.fetch_channel(main.origine(message.channel.id))
                await channel.send(main.echanger_mots(message.channel.id,message.guild.id))
                await message.channel.delete()
            else:
                main.confirmer_mot(message.channel.id)
          else :
            await message.channel.send("Veuillez proposer un mot avant de confirmer.")

        elif main.check_channels_echanges(message.guild.id,message.channel.id):
            if not main.check_mot(message.content, message.author.id,message.guild.id):
                await message.channel.send(f"Le dresseur <@{message.author.id}> ne possède pas le mot '{message.content.lower()}'. Veuillez rééssayer.")
            else:
                
                await message.channel.send(f"Le dresseur <@{message.author.id}> propose le mot '{message.content.lower()}' (rareté : `{main.changer_mot(message.channel.id,message.author.id,message.guild.id,message.content)}`) pour l'échange !")

        elif message.content == f"{main.get_prefix(message.guild.id)}quitter":
            await message.channel.send(f"<@{message.author.id}>, entrez `!confirmersuppression` afin de confirmer la suppression de votre profil de dresseur.")

        elif (message.content.startswith(f"{main.get_prefix(message.guild.id)}existe ") or message.content.startswith(f"{main.get_prefix(message.guild.id)}peutonpaké "))and message.content.split(" ")[1]:
          await message.channel.send(main.check_mot_existe(message.content.split(" ")[1]))
        
        elif message.content == (f"{main.get_prefix(message.guild.id)}confirmersuppression"):
          await message.channel.send(main.suppression_dresseur(message.author.id,message.guild.id))

        elif message.content.startswith(f"{main.get_prefix(message.guild.id)}upgrade"):
            try:
                await message.channel.send(main.upgrade(message.author.id,message.guild.id,int(message.content.split(" ")[1])))
            except:
                await message.channel.send(main.upgrade(message.author.id,message.guild.id))
        elif message.content.startswith(f"{main.get_prefix(message.guild.id)}info"):
            if not message.mentions:
              await message.channel.send(main.info(message.author.id,message.guild.id, message.author.name))
            elif main.check_dresseur_existe(message.mentions[0].id,message.guild.id):
              await message.channel.send(main.info(message.mentions[0].id,message.guild.id, message.mentions[0].name,message.author.id))
            else :
              await message.channel.send(f"Dresseur `{message.mentions[0].name}` introuvable.")

        elif message.content == f"{main.get_prefix(message.guild.id)}classement":
          stats,classement=main.classement(message.author.id,message.guild.id)
          newline='\n'
          await message.channel.send(f"<a:mokeball:958666482894643200>`CLASSEMENT DES DRESSEURS`<a:mokeball:958666482894643200>{newline*2}{newline.join([f'{numbers[i]} <@{classement[i][1]}> : {classement[i][2]}pts - {classement[i][3]} mots' for i in range(len(classement))])}{newline*2}`{stats[3]}` <@{message.author.id}> (Vous) : {stats[1]}pts - {stats[2]} mots")
          
        elif message.content == (f"{main.get_prefix(message.guild.id)}hauthautbasbasgauchedroitegauchedroiteBAstart"):
          await message.channel.send(main.cheatpoints(message.author.id,message.guild.id))
    if message.content:
      main.ajouterscore(message.author.id,message.guild.id, message.content)

keep_alive()
try:
  iencli.run(os.getenv('TOKEN'))
except discord.errors.HTTPException:
    print("\n\n\nBLOCKED BY RATE LIMITS\nRESTARTING NOW\n\n\n")
    os.system("python restarter.py")
    os.system('kill 1')