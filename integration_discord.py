import discord
import main

class leClient(discord.Client(activity=discord.Game(name='!help pour les commandes'))):
    def __init__(self):
        self.trade_en_cours=False
        self.proposition_trade=False
        self.dresseur1_trade=""
        self.dresseur2_trade=""
        self.dresseur1_mot=""
        self.dresseur2_mot=""
        self.dresseur1_complete=False
        self.dresseur2_complete=False
    async def on_ready(self):
        print(f'Logged in as {self.user.name} - {self.user.id}')
    async def on_message(self.message):
        if message.author.id == self.user.id :#empêcher que le bot ne détecte ses propres messages
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
        elif self.proposition_trade and message.author.id==dresseur2_trade and message.content=="!accepter":
            self.proposition_trade=False
            self.trade_en_cours=True
            await message.channel.send(f"Échange entre @{dresseur1} et @{dresseur2} commencé !\n\
entrez le mot que vous souhaitez échanger et utilisez tous les deux la commande ```!completer``` pour compléter.")

        elif self.proposition_trade and message.author.id==dresseur2_trade and message.content=="!refuser":
            self.proposition_trade=False
            await message.channel.send("Échange refusé.")

        elif self.trade_en_cours and message.author.id in [dresseur2_trade,dresseur1_trade] and message.content=="!annuler":
            self.trade_en_cours=False
            await message.channel.send("Échange annulé.")
            
        elif message.content=="!kukujariv":
            main.creer_dresseur(str(message.author.id))
            await message.channel.send(f"Dresseur @{message.author.id} créé ! Attrapez les tous ! :D")

        elif message.content=="!mokedex":
            main.afficher_mots(str(message.author.id))
            #await message.channel.send(f"Le dresseur @{message.author.id} possède les mots suivants : **{(', '.join([raw[0] for raw in record]))}**") CHANGER CA

        elif message.content=="!booster":
            main.ouverture_booster(str(message.author.id))
            await message.channel.send(f"Bravo @{message.author.id} ! tu obtiens les mots suivants : **{(', '.join([raw[0] for raw in record]))}**")

        elif message.content.startswith("!echange "):
            dresseur1_trade=message.author.id
            dresseur2_trade=message.content.split(" ")[1]
            if message.guild.get_member(dresseur2_trade) is not None: await message.channel.send(f"Le dresseur @{dresseur1_trade} propose un **échange** avec le dresseur @{dresseur2_trade} !\
@{dresseur2_trade}, utilisez la commandes ```!accepter``` ou ```!refuser```.")
            else : await message.channel.send(f"Dresseur '{dresseur2_trade}' introuvable.")

        #elif message.content.startswith("!mokedex"):
            #main.afficher_mots(str(message.author.id))
            #await message.channel.send(f"Le dresseur @{message.author.id} possède les mots suivants : {(', '.join([raw[0] for raw in record]))}")

        
iencli=leClient()
iencli.run('token')
    
print(f"mots {(', '.join([mot for mot in mots]))} capturés.")
