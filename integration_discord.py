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

prefix="!"

@iencli.event
async def on_ready():
    print(f'Logged in as {iencli.user.name} - {iencli.user.id}')

@iencli.event
async def on_message(message):
    global trade_en_cours,proposition_trade,dresseur1_trade,dresseur2_trade,dresseur1_mot,dresseur2_mot,half_complete
    if message.author.id == iencli.user.id :#empêcher que le bot ne détecte ses propres messages
        return None

    elif message.content==f"{prefix}help":
        await message.channel.send(f"**Commandes du bot Wordpacks**\n\n\
```{prefix}help``` - afficher cette page\n\
```{prefix}kukujariv``` - s'inscrire en tant que dresseur\n\
```{prefix}mokedex``` - afficher les mots que vous possédez\n\
```{prefix}booster``` - ouvrir un booster de 3 mots\n\
```{prefix}echange [dresseur]``` - proposer un échange avec un dresseur\n\
```{prefix}accepter``` - accepter la proposition d'échange\n\
```{prefix}refuser``` - refuser la proposition d'échange\n\
```{prefix}annuler``` - annuler l'échange\n\
```{prefix}completer``` - compléter l'échange")
    elif proposition_trade and message.author.id==dresseur2_trade and message.content=="{prefix}accepter":
        proposition_trade=False
        trade_en_cours=True
        await message.channel.send(f"Échange entre <@{dresseur1_trade}> et <@{dresseur2_trade}> commencé !\n\
entrez le mot que vous souhaitez échanger et utilisez tous les deux la commande ```{prefix}completer``` pour compléter.")

    elif proposition_trade and message.author.id==dresseur2_trade and message.content=="{prefix}refuser":
        proposition_trade=False
        await message.channel.send("Échange refusé.")

    elif trade_en_cours and message.author.id in [dresseur2_trade,dresseur1_trade] and message.content=="{prefix}annuler":
        trade_en_cours=False
        await message.channel.send("Échange annulé.")
        
    elif message.content=="{prefix}kukujariv":
        main.creer_dresseur(str(message.author.id))
        await message.channel.send(f"Dresseur <@{message.author.id}> créé ! Attrapez les tous !")

    elif message.content=="{prefix}mokedex":
        record=main.afficher_mots(str(message.author.id))
        await message.channel.send(f"Le dresseur <@{message.author.id}> possède les mots suivants : **{(', '.join([raw[0] for raw in record]))}**")

    elif message.content=="{prefix}booster":
        record=main.ouverture_booster(str(message.author.id))
        print(record)
        await message.channel.send(f"Bravo <@{message.author.id}> ! tu obtiens les mots suivants : **{(', '.join(record))}**")

    elif message.content.startswith("{prefix}echange ") and message.content.split(" ")[1]!=message.content.split(" ")[0]:
        dresseur1_trade=message.author.id
        dresseur2_trade=message.content.split(" ")[1]
        if message.guild.get_member(dresseur2_trade) is not None: await message.channel.send(f"Le dresseur <@{dresseur1_trade}> propose un **échange** avec le dresseur <@{dresseur2_trade}> !\
<@{dresseur2_trade}>, utilisez la commandes ```{prefix}accepter``` ou ```{prefix}refuser```.")
        else : await message.channel.send(f"Dresseur '{dresseur2_trade}' introuvable.")

    elif trade_en_cours and message.author.id in [dresseur1_trade,dresseur2_trade] and [dresseur1_mot,dresseur2_mot][[dresseur1_trade,dresseur2_trade].index(message.author.id)]!="" and message.content=="{prefix}completer":
        await message.channel.send(f"Le dresseur <@{message.author.id}> bloque le mot '{[dresseur1_mot,dresseur2_mot][[dresseur1_trade,dresseur2_trade].index(message.author.id)]}'.")
        if half_complete:
            await message.channel.send(main.echanger_mots(dresseur1_mot,dresseur2_mot,dresseur1_trade,dresseur2_trade))
        else : half_complete=True

    elif trade_en_cours and message.author.id in [dresseur1_trade,dresseur2_trade]:
        [dresseur1_mot,dresseur2_mot][[dresseur1_trade,dresseur2_trade].index(message.author.id)]=main.check_mot(mot,message.author.id)
        if [dresseur1_mot,dresseur2_mot][[dresseur1_trade,dresseur2_trade].index(message.author.id)]=="":
            await message.channel.send(f"Le dresseur <@{message.author.id}> ne possède pas le mot '{message.content}'. Veuillez rééssayer.")
        else : await message.channel.send(f"Le dresseur <@{message.author.id}> propose le mot '{message.content}' pour l'échange !")

keep_alive()
iencli.run(os.getenv('TOKEN'))
