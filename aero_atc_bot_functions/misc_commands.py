import discord.app_commands, discord.utils
from discord import Interaction, ForumChannel, CategoryChannel
from random import randint
from typing import List
from .permissions import has_any_role, RoleIDs

@discord.app_commands.command(description="Ping the bot and it will say \"Pong!\" in response")
@has_any_role(RoleIDs.VERIFIED)
async def ping(ctx: Interaction):

    await ctx.response.send_message("Pong!")

@discord.app_commands.command(description="Gives the current time in UTC/GMT")
@has_any_role(RoleIDs.VERIFIED)
async def utc(ctx: Interaction):

    await ctx.response.send_message(f"{discord.utils.utcnow().strftime("%H%Mz")}")

@discord.app_commands.command(description="Generate a 4 digit squawk code. Does not check for invalid codes")
@has_any_role(RoleIDs.VERIFIED)
async def generate_squawk(ctx: Interaction):

    squawk: str = ""
    for i in range(4):
        squawk += str(randint(0,7))
    await ctx.response.send_message(squawk)

@discord.app_commands.command(description="Makes the bot say the given message")
@has_any_role(RoleIDs.DIRECTORS)
async def say(ctx: Interaction, message: str):

    if not (isinstance(ctx.channel, ForumChannel) or isinstance(ctx.channel, CategoryChannel)):
        if ctx.channel is not None:
            await ctx.response.send_message("Message sucessfully sent", ephemeral=True, delete_after=3)
            await ctx.channel.send(message)
        else:
            await ctx.response.send_message("An unknown error has occured", ephemeral=True)
    else:
        await ctx.response.send_message("Channel type unsupported", ephemeral=True)