import discord
import main

class leClient(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user.name} - {self.user.id}')
    async def on_message(self.message):
        if message.author.id == self.user.id #empêcher que le bot ne détecte ses propres messages
            return None
        if message.content.startswith("!mokedex"):
            main.ouverture_booster
            await message.channel.send(f"Le dresseur {nom_dresseur} possède les mots suivants : {(', '.join([raw[0] for raw in record]))}")
        
client=leClient()
client.run('token')
    
print(f"mots {(', '.join([mot for mot in mots]))} capturés.")
