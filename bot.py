# My database server id: 770442539760746526
# Aeronautica ATC server id: 1120012114321494088

import discord
from discord.ext import commands
import time
import typing
import bot_functions

intents = discord.Intents.default()
intents.message_content = True

guilds: list = [discord.Object(id=770442539760746526), discord.Object(id=1120012114321494088)]

bot: commands.Bot = commands.Bot(command_prefix="!", intents=intents)

"""
This command sends "Pong!" to the same channel that the command is run in
"""
@bot.tree.command(name="ping", description="Ping the bot and it will ping back", guilds=guilds)
async def ping(ctx: discord.Interaction):
    await ctx.response.send_message("Pong!")

"""
This command is a testing command for parameters testing
"""
@bot.tree.command(name="paramtest", description="Testing for parameters", guilds=guilds)
async def paramtest(ctx: discord.Interaction, arg: str):
    await ctx.response.send_message(f"{arg}")

"""
This command takes an airport code and returns all positions that could control that airport WIP
"""
@bot.tree.command(name="positions", description="Find all the positions that control an airport", guilds=guilds)
async def find_frequency(ctx: discord.Interaction, airport: str):
    await ctx.response.send_message(bot_functions.find_frequency(airport))

"""
This command returns the time in UTC in the form HHMMz
"""
@bot.tree.command(name="utc", description="Find the current time in UTC", guilds=guilds)
async def send_time_utc(ctx: discord.Interaction):
    await ctx.response.send_message(bot_functions.get_time_utc())

"""
This command returns a random squawk code, does not check for invalid codes
"""
@bot.tree.command(name="squawk", description="Generate a random sqawk code", guilds=guilds)
async def squawk(ctx: discord.Interaction):
    await ctx.response.send_message(bot_functions.generate_squawk())

@bot.tree.command(name="generate_atis", description="Generates an ATIS from input information", guilds=guilds)
async def gen_atis(ctx: discord.Interaction):
    await ctx.response.send_message(bot_functions.generate_atis())

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