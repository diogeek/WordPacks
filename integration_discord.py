import discord
import os
import main

iencli = discord.Client()

trade_en_cours=False
proposition_trade=False
dresseur1_trade=""
dresseur2_trade=""
dresseur1_mot=""
dresseur2_mot=""
half_complete=False

@iencli.event
async def on_ready(self):275146542144
    print(f'Logged in as {user.name} - {user.id}')

@iencli.event
async def on_message(message):
    if message.author.id == user.id :#empêcher que le bot ne détecte ses propres messages
        return None

    elif message.content=="!help":
        await message.channel.send("**Commandes du bot Wordpacks**\n\n\
```!help``` - afficher cette page\n\
```!kukujariv``` - s'inscrire en tant que dresseur\n\
```!mokedex``` - afficher les mots que vous possédez\n\
```!booster``` - ouvrir un booster de 3 mots\n\
```!echange [dresseur]``` - proposer un échange avec un dresseur\n\
```!accepter``` - accepter la proposition d'échange\n\
```!refuser``` - refuser la proposition d'échange\n\
```!annuler``` - annuler l'échange\n\
```!completer``` - compléter l'échange")
    elif proposition_trade and message.author.id==dresseur2_trade and message.content=="!accepter":
        proposition_trade=False
        trade_en_cours=True
        await message.channel.send(f"Échange entre @{dresseur1} et @{dresseur2} commencé !\n\
entrez le mot que vous souhaitez échanger et utilisez tous les deux la commande ```!completer``` pour compléter.")

    elif proposition_trade and message.author.id==dresseur2_trade and message.content=="!refuser":
        proposition_trade=False
        await message.channel.send("Échange refusé.")

    elif trade_en_cours and message.author.id in [dresseur2_trade,dresseur1_trade] and message.content=="!annuler":
        trade_en_cours=False
        await message.channel.send("Échange annulé.")
        
    elif message.content=="!kukujariv":
        main.creer_dresseur(str(message.author.id))
        await message.channel.send(f"Dresseur @{message.author.id} créé ! Attrapez les tous !")

    elif message.content=="!mokedex":
        record=main.afficher_mots(str(message.author.id))
        await message.channel.send(f"Le dresseur @{message.author.id} possède les mots suivants : **{(', '.join([raw[0] for raw in record]))}**")

    elif message.content=="!booster":
        record=main.ouverture_booster(str(message.author.id))
        await message.channel.send(f"Bravo @{message.author.id} ! tu obtiens les mots suivants : **{(', '.join([raw[0] for raw in record]))}**")

    elif message.content.startswith("!echange "):
        dresseur1_trade=message.author.id
        dresseur2_trade=message.content.split(" ")[1]
        if message.guild.get_member(dresseur2_trade) is not None: await message.channel.send(f"Le dresseur @{dresseur1_trade} propose un **échange** avec le dresseur @{dresseur2_trade} !\
@{dresseur2_trade}, utilisez la commandes ```!accepter``` ou ```!refuser```.")
        else : await message.channel.send(f"Dresseur '{dresseur2_trade}' introuvable.")

    elif trade_en_cours and message.author.id in [dresseur1_trade,dresseur2_trade] and [dresseur1_mot,dresseur2_mot][[dresseur1_trade,dresseur2_trade].index(message.author.id)]!="" and message.content=="!completer":
        await message.channel.send(f"@{message.author.id} bloque le mot '{[dresseur1_mot,dresseur2_mot][[dresseur1_trade,dresseur2_trade].index(message.author.id)]}'.")
        if half_complete:
            await message.channel.send(main.echanger_mots(dresseur1_mot,dresseur2_mot,dresseur1_trade,dresseur2_trade))
        else : half_complete=True

    elif trade_en_cours and message.author.id in [dresseur1_trade,dresseur2_trade]:
        [dresseur1_mot,dresseur2_mot][[dresseur1_trade,dresseur2_trade].index(message.author.id)]=check_mot(mot,message.author.id)
        if [dresseur1_mot,dresseur2_mot][[dresseur1_trade,dresseur2_trade].index(message.author.id)]=="":
            await message.channel.send(f"Le dresseur @{message.author.id} ne possède pas le mot '{message.content}'. Veuillez rééssayer.")
        else : await message.channel.send(f"Le dresseur @{message.author.id} propose le mot '{message.content}' pour l'échange !")

iencli.run(os.getenv('ba4096d46aa2f237feca511cd518260010a92504d2ec588a5711b1f562de2aa2'))
    
print(f"mots {(', '.join([mot for mot in mots]))} capturés.")
