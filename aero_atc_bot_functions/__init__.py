from typing import List
from discord.app_commands import Command
from .misc_commands import ping, utc, generate_squawk, say
from .atis import generate_atis, edit_atis, delete_atis

# IMPORTANT: All commands in the library MUST be added to this list, otherwise they will not be loaded at runtime
ALL_COMMANDS: List[Command] = [ping, utc, generate_squawk, say, generate_atis, edit_atis, delete_atis]