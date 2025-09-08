# My database server id: 770442539760746526
# Aeronautica ATC server id: 1120012114321494088

import discord
from discord.ext import commands
import os
from typing import List, Literal
import bot_functions
import pickle
import discord.enums

intents = discord.Intents.default()
intents.message_content = True
guilds: list = [discord.Object(id=1120012114321494088)] #discord.Object(id=770442539760746526),]
bot: commands.Bot = commands.Bot(command_prefix="!", intents=intents)
perms = [1175138965054042212, 1175139363961712730]

def check_permissions(ctx: discord.Interaction, roles: List[int]):
    user_roles: List[discord.Role] = ctx.user.roles # type: ignore
    for role in roles:
        for user_role in user_roles:
            if user_role.id == role:
                return True
    return False

@bot.tree.command(name="ping", description="Ping the bot and it will ping back", guilds=guilds)
async def ping(ctx: discord.Interaction):
    if not check_permissions(ctx, perms):
        await ctx.response.send_message("You do not have permission to use this command", ephemeral=True)
        return
    await ctx.response.send_message("Pong!")

@bot.tree.command(name="positions", description="Find all the positions that control an airport", guilds=guilds)
async def find_frequency(ctx: discord.Interaction, airport: str):
    if not check_permissions(ctx, perms):
        await ctx.response.send_message("You do not have permission to use this command", ephemeral=True)
        return
    await ctx.response.send_message(bot_functions.find_frequency(airport))

@bot.tree.command(name="utc", description="Find the current time in UTC", guilds=guilds)
async def send_time_utc(ctx: discord.Interaction):
    if not check_permissions(ctx, perms):
        await ctx.response.send_message("You do not have permission to use this command", ephemeral=True)
        return
    await ctx.response.send_message(bot_functions.get_time_utc())

@bot.tree.command(name="squawk", description="Generate a random sqawk code", guilds=guilds)
async def squawk(ctx: discord.Interaction):
    if not check_permissions(ctx, perms):
        await ctx.response.send_message("You do not have permission to use this command", ephemeral=True)
        return
    await ctx.response.send_message(bot_functions.generate_squawk())

@bot.tree.command(name="generate_atis", description="Generates an ATIS from input information", guilds=guilds)
async def gen_atis(ctx: discord.Interaction, airport: str, wind: str, temp: str, dewpoint: str, pressure:str, clouds: str, visibility: str, runway: str, dispatch_station: str = "UNICOM", dispatch_frequency: str = "122.800", dep_runway: str = ""):
    if not check_permissions(ctx, perms):
        await ctx.response.send_message("You do not have permission to use this command", ephemeral=True)
        return
    atis: bot_functions.ATIS = bot_functions.ATIS(airport, wind, temp, dewpoint, pressure, clouds, visibility, dispatch_station, dispatch_frequency, runway, dep_runway)
    try:
        file = open(f"atis_database/{airport.lower()}.atis", "xb")
        file.close()
    except FileExistsError as e:
        await ctx.response.send_message(f"An ATIS already exists for {atis.airport.upper()}, try /edit_atis or /delete_atis")
        return
    try:
        await ctx.response.send_message(atis.to_string())
        response: discord.InteractionMessage = await ctx.original_response()
        atis.channel = response.channel.id
        atis.message = response.id
        file = open(f"atis_database/{airport.lower()}.atis", "wb")
        pickle.dump(obj=atis, file=file)
        file.close()
        return
    except Exception as e:
        print(e)
        return
    
@bot.tree.command(name="delete_atis", description="Deletes an ATIS for an airport", guilds=guilds)
async def delete_atis(ctx: discord.Interaction, airport: str):
    if not check_permissions(ctx, perms):
        await ctx.response.send_message("You do not have permission to use this command", ephemeral=True)
        return
    if os.path.exists(f"atis_database/{airport.lower()}.atis"):
        try:
            os.remove(f"atis_database/{airport.lower()}.atis")
            await ctx.response.send_message(f"ATIS for {airport.upper()} has been deleted")
        except Exception as e:
            await ctx.response.send_message("An unknown error has occured")
    else:
        await ctx.response.send_message(f"No ATIS exists for {airport.upper()}, use /generate_atis to create one")

@bot.tree.command(name="edit_atis", description="Edit an already existing ATIS", guilds=guilds)
async def edit_atis(ctx: discord.Interaction, airport: str, option: Literal["wind", "temperature", "dewpoint", "pressure", "clouds", "visibility", "runway", "departure_runway", "dispatch_station", "dispatch_frequency", "pdc_availability", "server_code"], value: str, update_letter: bool=False):
    try:
        file = open(f"atis_database/{airport.lower()}.atis", "rb")
        atis: bot_functions.ATIS = pickle.load(file)
        file.close()
        atis.edit_atis(option, value)
        channel = await bot.fetch_channel(atis.channel)
        message = await channel.fetch_message(atis.message) # type: ignore
        await message.edit(content=atis.to_string())
        await ctx.response.send_message("Value edited successfully", ephemeral=True, delete_after=5)
        file = open(f"atis_database/{airport.lower()}.atis", "wb")
        pickle.dump(obj=atis, file=file)
        file.close()
    except Exception as e:
        raise e

@bot.tree.command(name="say", description="Says something in the provided channel id or in the current channel", guilds=guilds)
async def say(ctx: discord.Interaction, message: str, channel_id: str="0"):
    if not check_permissions(ctx, perms):
        await ctx.response.send_message("You do not have permission to use this command", ephemeral=True)
        return
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

@bot.tree.command(name="delete_all_atis", description="Deletes all active ATIS's", guilds=guilds)
async def delete_all_atis(ctx: discord.Interaction):
    file_list = os.listdir("atis_database")
    i = 0
    for file_name in file_list:
        file = open(f"atis_database/{file_name}", "rb")
        atis: bot_functions.ATIS = pickle.load(file)
        channel = await bot.fetch_channel(atis.channel)
        message = await channel.fetch_message(atis.message) # type: ignore
        await message.delete()
        file.close()
        os.remove(f"atis_database/{file_name}")
        i += 1
    await ctx.response.send_message(f"Successfully deleted {i} ATIS(s)", ephemeral=True)


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