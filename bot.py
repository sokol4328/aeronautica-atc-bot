# My database server id: 770442539760746526
# Aeronautica ATC server id: 1120012114321494088

import discord
from discord.ext import commands
import time
import typing
import bot_functions

intents = discord.Intents.default()
intents.message_content = True

guilds: list = [discord.Object(id=770442539760746526)]#, discord.Object(id=1120012114321494088)]

bot: commands.Bot = commands.Bot(command_prefix="!", intents=intents)

@bot.tree.command(name="ping", description="Ping the bot and it will ping back", guilds=guilds)
async def ping(ctx: discord.Interaction):
    await ctx.response.send_message("Pong!")

@bot.tree.command(name="paramtest", description="Testing for parameters", guilds=guilds)
async def paramtest(ctx: discord.Interaction, arg: str):
    await ctx.response.send_message(f"{arg}")

@bot.tree.command(name="positions", description="Find all the positions that control an airport", guilds=guilds)
async def find_frequency(ctx: discord.Interaction, airport: str):
    await ctx.response.send_message(bot_functions.find_frequency(airport))

@bot.tree.command(name="utc", description="Find the current time in UTC", guilds=guilds)
async def send_time_utc(ctx: discord.Interaction):
    await ctx.response.send_message(bot_functions.get_time_utc())

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    for guild in guilds:
        await bot.tree.sync(guild=guild)
        print(f"Commands loaded for guild {guild.id}")
    print("Loading complete, bot is online")

file = open("token.txt", "r")
token = file.read()
bot.run(token=token)