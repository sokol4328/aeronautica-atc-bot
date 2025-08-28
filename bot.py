# My database server id: 770442539760746526
# Aeronautica ATC server id: 1120012114321494088

import discord
import time

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

@tree.command(name="ping", description="Ping the bot and it will ping back", guild=discord.Object(id=770442539760746526))
async def ping(interaction):
    await interaction.response.send_massage("Ping!")

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    await tree.sync(guild=discord.Object(id=770442539760746526))
    print("Commands loaded for testing server")
    #await tree.sync(guild=discord.Object(id=1120012114321494088))
    #print("Commands loaded for Aeronautica ATC server")

    print("Loading complete, bot is online")

file = open("token.txt", "r")
token = file.read()
client.run(token=token)