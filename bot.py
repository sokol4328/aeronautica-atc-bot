from discord.ext.commands.bot import Bot
from discord.app_commands import Command, ContextMenu
import discord.utils
from discord import Object, Intents, Interaction, DMChannel
import aero_atc_bot_functions
from typing import Union
import json

with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

GUILD_ID = config["bot"]["guild_id"]
PREFIX = config["bot"]["prefix"]

class AeroATCBot(Bot):

    # This variable is a bit odd but in order to pass a guild id to the commands, the id must be a discord.py
    # object (small "o"). Thus, we create a basic Object class with the id of the AeroATC server and use that
    guild_id = Object(id=GUILD_ID)
    
    def __init__(self):
        super().__init__(command_prefix=PREFIX, intents=Intents.all())

    async def add_all_commands(self):
        for command in aero_atc_bot_functions.ALL_COMMANDS:
            self.tree.add_command(command, guild=self.guild_id)
        await self.tree.sync(guild=self.guild_id)
        print("Commands have been loaded")
    
    async def on_app_command_completion(self, interaction: Interaction, command: Union[Command, ContextMenu]):
        if interaction.command == None or interaction.channel == None or interaction.channel is DMChannel:
            print(f"Strange error occured, investigate:\nIn on_command in bot.py, None occured when it shouldn't have")
            return
        print(f"Command {interaction.command.name} was used by {interaction.user.name} " +
              f"in {interaction.channel.name} at {discord.utils.utcnow().time()}") # type: ignore

    async def on_ready(self):
        await self.add_all_commands()
        await self.change_presence(status=discord.Status("online"),
                                   activity=discord.Game(name=f"Watching over the AATC community"))
        print(f"Logged in as {self.user} at {discord.utils.utcnow().time()}")