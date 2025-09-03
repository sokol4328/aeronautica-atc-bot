# My database server id: 770442539760746526
# Aeronautica ATC server id: 1120012114321494088

import discord
from discord.ext import commands
import time
import threading
from typing import List
import bot_functions
import pickle

intents = discord.Intents.default()
intents.message_content = True
guilds: list = [discord.Object(id=1120012114321494088)] #discord.Object(id=770442539760746526),]
bot: commands.Bot = commands.Bot(command_prefix="!", intents=intents)

def check_permissions(ctx: discord.Interaction, roles: List[int]):
    user_roles: List[discord.Role] = ctx.user.roles # type: ignore
    for role in roles:
        for user_role in user_roles:
            if user_role.id == role:
                return True
    return False

"""
This command sends "Pong!" to the same channel that the command is run in
"""
@bot.tree.command(name="ping", description="Ping the bot and it will ping back", guilds=guilds)
async def ping(ctx: discord.Interaction):
    if not check_permissions(ctx, [1175139363961712730]):
        await ctx.response.send_message("You do not have permission to use this command", ephemeral=True)
    await ctx.response.send_message("Pong!")

"""
This command takes an airport code and returns all positions that could control that airport WIP
"""
@bot.tree.command(name="positions", description="Find all the positions that control an airport", guilds=guilds)
async def find_frequency(ctx: discord.Interaction, airport: str):
    if not check_permissions(ctx, [1175139363961712730]):
        await ctx.response.send_message("You do not have permission to use this command", ephemeral=True)
    await ctx.response.send_message(bot_functions.find_frequency(airport))

"""
This command returns the time in UTC in the form HHMMz
"""
@bot.tree.command(name="utc", description="Find the current time in UTC", guilds=guilds)
async def send_time_utc(ctx: discord.Interaction):
    if not check_permissions(ctx, [1175139363961712730]):
        await ctx.response.send_message("You do not have permission to use this command", ephemeral=True)
    await ctx.response.send_message(bot_functions.get_time_utc())

"""
This command returns a random squawk code, does not check for invalid codes
"""
@bot.tree.command(name="squawk", description="Generate a random sqawk code", guilds=guilds)
async def squawk(ctx: discord.Interaction):
    if not check_permissions(ctx, [1175139363961712730]):
        await ctx.response.send_message("You do not have permission to use this command", ephemeral=True)
    await ctx.response.send_message(bot_functions.generate_squawk())

"""
THis command makes an ATIS based on user given information. It also stores the generated ATIS via pickle.
"""
@bot.tree.command(name="generate_atis", description="Generates an ATIS from input information", guilds=guilds)
async def gen_atis(ctx: discord.Interaction, airport: str, wind: str, temp: str, dewpoint: str, pressure:str, clouds: str, visibility: str):
    if not check_permissions(ctx, [1175139363961712730]):
        await ctx.response.send_message("You do not have permission to use this command", ephemeral=True)
    atis: bot_functions.ATIS = bot_functions.ATIS(airport, wind, temp, dewpoint, pressure, clouds, visibility)
    try:
        file = open(f"atis_database/{airport.lower()}.atis", "x")
        file.close()
        file = open(f"atis_database/{airport.lower()}.atis", "wb")
        pickle.dump(obj=atis, file=file)
        await ctx.response.send_message(atis.to_string())
    except FileExistsError as e:
        await ctx.response.send_message(f"An ATIS already exists for {atis.airport.upper()}, try /edit_atis or /delete_atis")
    except Exception as e:
        print(e)

@bot.tree.command(name="say", description="Says something in the provided channel id", guilds=guilds)
async def say(ctx: discord.Interaction, message: str, channel_id: str="0"):
    if not check_permissions(ctx, [1175139363961712730, 1175139363961712730]):
        await ctx.response.send_message("You do not have permission to use this command", ephemeral=True)
    try:
        channel = None
        if channel_id == "0":
            channel = ctx.channel # type: ignore
        else:
            channel = bot.get_channel(int(channel_id)) # type: ignore
        await channel.send(message) # type: ignore
        await ctx.response.send_message(f"Message sent to <#{channel.id}>", ephemeral=True, delete_after=5) # type: ignore
    except Exception as e:
        await ctx.response.send_message("An unknown error has occured", ephemeral=True)
        print(e)


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