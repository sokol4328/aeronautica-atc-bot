import discord.app_commands
from discord import Interaction, ForumChannel, GroupChannel, CategoryChannel, Interaction, Message
from .permissions import check_permissions, Permissions
from .metar import Metar
from typing import Literal, cast
from random import randint
from time import time, gmtime, strftime
import pickle
from io import BufferedWriter, BufferedReader

class ATIS():

    def __init__(self, airport: str, runways: str, server_code: str, wind: str, temperature: str, dewpoint: str,
                 pressure: str, clouds: str, visibility: str, departure_runways: str, dispatch_station: str,
                 dispatch_frequency: str, transition_level: str, pdc: bool):
        self.airport: str = airport.upper()
        self.runways: str = runways.upper()
        self.server_code: str = server_code.upper()
        self.metar: Metar = Metar(pressure, wind, temperature, dewpoint, clouds, visibility)
        self.departure_runways: str = departure_runways.upper()
        self.dispatch_station: str = dispatch_station.upper()
        self.dispatch_frequency: str = dispatch_frequency
        self.transition_level: str = transition_level
        self.pdc: bool = pdc
        self.atis_letter: int = randint(0, 25)
        self.message_id: int

    # Eventually this method will automatically find the FIR of an airport based on the ICAO code TODO
    def fetch_fir(self) -> Literal["FAA", "CAA", "ICAO"]:
        return "FAA"
    
    # This method converts an integer 0-25 into the corresponding letter (1 being A, 2 being B and so on)
    def get_atis_letter(self) -> str:
        if self.atis_letter > 25:
            self.atis_letter = 0
        return chr(65 + self.atis_letter)
    
    # This method edits the ATIS object based on the "option" parameter
    def edit_atis(self, option: str, value: str) -> None:
        match option:
            case "wind":
                self.metar.wind = value
            case "temperature":
                self.metar.temperature = value
            case "dewpoint":
                self.metar.dewpoint = value
            case "pressure":
                self.metar.pressure = value
            case "clouds":
                self.metar.clouds = value
            case "visibility":
                self.metar.visibility = value
            case "runways":
                self.runways = value
            case "depature_runways":
                self.departure_runways = value
            case "dispatch_station":
                self.dispatch_station = value
            case "dispatch_frequency":
                self.dispatch_freq = value
            case "pdc_availability":
                if value == "True":
                    self.pdc = True
                else:
                    self.pdc = False
            case "server_code":
                self.server_code = value
    
    def to_string(self) -> str:
        atis: str = ""
        fir: Literal["FAA", "CAA", "ICAO"] = self.fetch_fir()
        match fir:

            # FAA Style ATIS
            case "FAA":
                atis += f"`{self.airport} ATIS INFO {self.get_atis_letter()} {strftime("%H%MZ", gmtime(time()))}\n"
                atis += self.metar.to_string("FAA") + "\n"
                approach = self.runways[0:3].upper()
                if approach != "ILS" or approach != "VOR" or approach != "RNV" or approach != "LOC":
                    atis += f"VISUAL APCH RWY(S) {self.runways}\n"
                else:
                    atis += f"{approach} APCH RWY(S) {self.runways[4:]}\n"
                if self.departure_runways != "":
                    atis += f"DEP RWY(S) {self.departure_runways}\n"
                atis += f"READBACK ALL RUNWAY HOLD SHORT INSTRUCTIONS\n"
                atis += f"CONTACT {self.dispatch_station} ON {self.dispatch_frequency} FOR CLNC\n"
                atis += f"TEXT PILOTS USE `<#1253808325129408552>` | "
                if self.pdc:
                    atis += f"PDC AVAIL\n"
                else:
                    atis += f"PDC UNAVAIL\n"
                atis += f"SERVER CODE {self.server_code}\n"
                atis += f"...ADVIS YOU HAVE {self.get_atis_letter()}`"
                return atis
            
            # CAA Style ATIS TODO
            case "CAA":
                atis += f"`{self.airport} ATIS INFO {self.get_atis_letter()} TIME {strftime("%H%MZ", gmtime(time()))}\n"
                if self.departure_runways == "":
                    atis += f"DEP RWY {self.runways} ARR RWY {self.runways} IN USE\n"
                else:
                    atis += f"DEP RWY {self.departure_runways} ARR RWY {self.runways} IN USE\n"
                atis += (self.metar.to_string("CAA") + "\n")
                if self.transition_level == "":
                    atis += f"TRANSITION LEVEL 060\n"
                else:
                    atis += f"TRANSITION LEVEL {self.transition_level}\n"
                atis += f"ACKNOWLEDGE RECEIPT OF INFORMATION {self.get_atis_letter()}\n"
                atis += f"AND ADVISE AFCT TYPE ON FIRST CONTACT WITH {self.airport}\n"
                atis += f"TEXT PILOTS USE `<#1253808325129408552>` | "
                if self.pdc:
                    atis += f"PDC AVAIL\n"
                else:
                    atis += f"PDC UNAVAIL\n"
                atis += f"SERVER CODE {self.server_code}`"
                return atis

            # ICAO Style ATIS TODO
            case "ICAO":
                atis += f"`{self.airport} ATIS {self.get_atis_letter()} {strftime("%H%MZ", gmtime(time()))}\n"
                if self.departure_runways == "":
                    atis += f"DEPARTURES {self.runways}. ARRIVALS {self.runways}\n"
                else:
                    atis += f"DEP RWY {self.departure_runways} ARR RWY {self.runways} IN USE\n"
                approach = self.runways[0:3].upper()
                if approach != "ILS" or approach != "VOR" or approach != "RNV" or approach != "LOC":
                    atis += f"EXP VISUAL APCH\n"
                else:
                    atis += f"EXP {approach} APCH\n"
                self.metar.to_string("ICAO")
                atis += f"TEXT PILOTS USE `<#1253808325129408552>` | "
                if self.pdc:
                    atis += f"PDC AVAIL\n"
                else:
                    atis += f"PDC UNAVAIL\n"
                atis += f"SERVER CODE {self.server_code}"
                atis += f"ACKNOWLEDGE INFO {self.get_atis_letter()} ON FIRST CTC WITH APP OR DEL`"
                return atis


@discord.app_commands.command(description="Creates a new airport ATIS")
async def generate_atis(ctx: Interaction, airport: str, runways: str, server_code: str, pressure: str, wind: str = "",
                        temperature: str = "", dewpoint: str = "", clouds: str = "", visibility: str = "",
                        departure_runways: str = "", dispatch_station: str = "UNICOM",
                        dispatch_frequency: str = "122.800", transition_level: str = "", pdc: bool = False):
    
    # Checking the user has the correct permissions
    if not await check_permissions(ctx, Permissions.CONTROLLERS_ONLY):
        return
    
    #Creating the ATIS object
    atis = ATIS(airport, runways, server_code, wind, temperature, dewpoint, pressure, clouds, visibility,
                departure_runways, dispatch_station, dispatch_frequency, transition_level, pdc)
    
    # Dumping the ATIS object into a pickle file for storage in the database
    try:
        atis_file: BufferedWriter = open(f".atis_database/{airport}.atis", "xb")
        reponse = await ctx.response.send_message(atis.to_string())
        atis.message_id = cast(int, reponse.message_id)
        pickle.dump(atis, atis_file)
    
    # If an ATIS already exists, the user will be informed
    except FileExistsError:
        await ctx.response.send_message("ATIS already exists for airport, try delete_atis or edit_atis instead",
                                        ephemeral=True)
        return

@discord.app_commands.command(description="Edit an already existing ATIS")
async def edit_atis(ctx: discord.Interaction, airport: str,
                    option: Literal["wind", "temperature", "dewpoint", "pressure", "clouds", "visibility", "runways",
                                    "departure_runways", "dispatch_station", "dispatch_frequency", "pdc_availability",
                                    "server_code"],
                    value: str, update_letter: bool=False):
    
    # Checking the user has the correct permissions
    if not await check_permissions(ctx, Permissions.CONTROLLERS_ONLY):
        return
    
    # Loading the ATIS from the database, or informing the user if it does not exist
    try:
        atis_r_file: BufferedReader = open(f".atis_database/{airport}.atis", "rb")
        atis: ATIS = pickle.load(atis_r_file)
        atis_r_file.close()
    except FileNotFoundError:
        await ctx.response.send_message("ATIS for airport not found, try generate_atis instead", ephemeral = True)
        return
    
    # Editing the ATIS and updating the ATIS letter if requested
    atis.edit_atis(option, value)
    if update_letter:
        atis.atis_letter += 1
    
    # Finding the original message, command must be executed in the same channel as the original message
    channel = ctx.channel
    if isinstance(channel, ForumChannel) or isinstance(channel, CategoryChannel) or isinstance(channel, GroupChannel):
        print(f"Strange error occured, investigate:\nLine 140 in atis.py, expected type not found")
        await ctx.response.send_message("Cannot edit ATIS in this type of channel", ephemeral = True)
        return
    if channel is not None:
        original_atis_partial = channel.get_partial_message(atis.message_id)
        original_atis: Message = cast(Message, await original_atis_partial.fetch())
        # Updaing the original message
        await original_atis.edit(content = atis.to_string())
    else:
        await ctx.response.send_message("Unknown error has occured", ephemeral=True)
        print(f"Strange error occured, investigate:\nLine 143 in atis.py, None occured when it shouldn't have")
        return
    
    # Re-opening the ATIS database file and rewritting it with the new information
    try:
        atis_w_file: BufferedWriter = open(f".atis_database/{airport}.atis", "wb")
        pickle.dump(atis, atis_w_file)
        atis_w_file.close()
    except Exception as e:
        await ctx.response.send_message("An unknown error has occured while writing to the ATIS database",
                                        ephemeral=True)
        print(f"Strange error occured, investigate:\n{e}")
        return