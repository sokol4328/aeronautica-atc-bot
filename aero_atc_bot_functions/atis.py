import discord.app_commands
from discord import ForumChannel, GroupChannel, CategoryChannel, Interaction, Message
from .permissions import has_role, RoleIDs
from typing import Literal, cast
from random import randint
from time import time, gmtime, strftime
import json
from io import TextIOWrapper, BufferedReader
import os

class ATIS():

    def __init__(self, airport: str, runways: str, server_code: str, wind: str, temperature: str, dewpoint: str,
                 pressure: str, weather_observations: str, clouds: str, visibility: str, departure_runways: str,
                 clearance_station: str, clearance_frequency: str, transition_level: str, pdc: bool, atis_letter: int,
                 message_id: int):
        self.airport: str = airport.upper()
        self.runways: str = runways.upper()
        self.server_code: str = server_code.upper()
        self.pressure: str = pressure
        self.weather_observations: str = weather_observations
        self.wind: str = wind
        self.temperature: str = temperature
        self.dewpoint: str = dewpoint
        self.clouds: str = clouds
        self.visibility: str = visibility
        self.departure_runways: str = departure_runways.upper()
        self.clearance_station: str = clearance_station.upper()
        self.clearance_frequency: str = clearance_frequency
        self.transition_level: str = transition_level
        self.pdc: bool = pdc
        if atis_letter != -1:
            self.atis_letter: int = randint(0, 25)
        else:
            self.atis_letter = atis_letter
        self.message_id = message_id

    # Eventually this method will automatically find the FIR of an airport based on the ICAO code, TODO
    def get_fir(self) -> Literal["FAA", "CAA", "ICAO"]:
        return "CAA"
    
    # This method converts an integer 0-25 into the corresponding letter (1 being A, 2 being B and so on)
    def get_atis_letter(self) -> str:
        if self.atis_letter > 25:
            self.atis_letter = 0
        return chr(65 + self.atis_letter)
    
    # This method edits the ATIS object based on the "option" parameter
    def edit_atis(self, option: str, value: str) -> None:
        match option:
            case "wind":
                self.wind = value
            case "temperature":
                self.temperature = value
            case "dewpoint":
                self.dewpoint = value
            case "pressure":
                self.pressure = value
            case "weather_observations":
                self.weather_observations = value
            case "clouds":
                self.clouds = value
            case "visibility":
                self.visibility = value
            case "runways":
                self.runways = value
            case "depature_runways":
                self.departure_runways = value
            case "clearance_station":
                self.clearance_station = value
            case "clearance_frequency":
                self.clearance_freq = value
            case "pdc_availability":
                if value == "True":
                    self.pdc = True
                else:
                    self.pdc = False
            case "server_code":
                self.server_code = value

    def metar(self, fir: Literal["FAA", "CAA", "ICAO"]):

        metar: str = ""

        if (self.wind == "" and self.temperature == "" and self.dewpoint == "" and self.weather_observations == "" and
                self.clouds == "" and self.visibility == ""):
            if fir == "FAA":
                return f"METAR UNAVAIL A{self.pressure}"
            return f"METAR UNAVAIL QNH {self.pressure}"
        
        match fir:
            case "FAA":
                if self.wind == "":
                    metar += "WIND UNAVAIL "
                else:
                    metar += f"{self.wind}KT "
                if self.visibility == "":
                    metar += "VISIBILITY UNAVAIL "
                else:
                    metar += f"{self.visibility}SM "
                if self.weather_observations == "":
                    pass
                else:
                    metar += f"{self.weather_observations} "
                if self.clouds == "":
                    metar += "CLOUDS UNAVAIL "
                else:
                    metar += f"{self.clouds} "
                if self.temperature == "":
                    metar += "TEMPERATURE UNAVAIL/"
                else:
                    metar += f"{self.temperature}/"
                if self.dewpoint == "":
                    metar += "DEWPOINT UNAVAIL "
                else:
                    metar += f"{self.dewpoint} "
                metar += f"A{self.pressure}"
            case "CAA":
                if self.wind == "":
                    metar += "/////KT "
                else:
                    metar += f"{self.wind}KT "
                if self.visibility == "":
                    metar += "////M "
                else:
                    metar += f"{self.visibility} "
                if self.weather_observations == "":
                    pass
                else:
                    metar += f"{self.weather_observations} "
                if self.clouds == "":
                    metar += "////// "
                else:
                    metar += f"{self.clouds} "
                if self.temperature == "":
                    metar += "///"
                else:
                    metar += f"{self.temperature}/"
                if self.dewpoint == "":
                    metar += "// "
                else:
                    metar += f"{self.dewpoint} "
                metar += f"QNH {self.pressure}"
            case "ICAO":
                if self.wind == "":
                    metar += "/////KT "
                else:
                    metar += f"WIND {self.wind}KT "
                if self.visibility == "":
                    metar += "////M "
                else:
                    metar += f"VIS {self.visibility}M "
                if self.weather_observations == "":
                    pass
                else:
                    metar += f"{self.weather_observations} "
                if self.clouds == "":
                    metar += "////// "
                else:
                    metar += f"{self.clouds} "
                if self.temperature == "":
                    metar += "/// "
                else:
                    metar += f"T{self.temperature} "
                if self.dewpoint == "":
                    metar += "// "
                else:
                    metar += f"D{self.dewpoint} "
                metar += f"QNH {self.pressure}"
        return metar
    
    def to_string(self) -> str:
        atis: str = ""
        fir: Literal["FAA", "CAA", "ICAO"] = self.get_fir()
        match fir:

            # FAA Style ATIS
            case "FAA":
                atis += f"`{self.airport} ATIS INFO {self.get_atis_letter()} {strftime('%H%MZ', gmtime(time()))}\n"
                atis += self.metar("FAA") + "\n"
                approach: str = self.runways[0:3].upper()
                if approach == "ILS" or approach == "VOR" or approach == "RNV" or approach == "LOC":
                    atis += f"{approach} APCH RWY(S) {self.runways[4:]}\n"
                else:
                    atis += f"VISUAL APCH RWY(S) {self.runways}\n"
                if self.departure_runways != "":
                    atis += f"DEP RWY(S) {self.departure_runways}\n"
                atis += f"READBACK ALL RUNWAY HOLD SHORT INSTRUCTIONS\n"
                atis += f"CONTACT {self.clearance_station} ON {self.clearance_frequency} FOR CLNC\n"
                atis += f"TEXT PILOTS USE `<#1253808325129408552>` | "
                if self.pdc:
                    atis += f"PDC AVAIL\n"
                else:
                    atis += f"PDC UNAVAIL\n"
                atis += f"SERVER CODE {self.server_code}\n"
                atis += f"...ADVIS YOU HAVE {self.get_atis_letter()}`"
                return atis
            
            # CAA Style ATIS
            case "CAA":
                atis += f"`{self.airport} ATIS INFO {self.get_atis_letter()} TIME {strftime('%H%MZ', gmtime(time()))}\n"
                if self.departure_runways == "":
                    atis += f"DEP RWY {self.runways} ARR RWY {self.runways} IN USE\n"
                else:
                    atis += f"DEP RWY {self.departure_runways} ARR RWY {self.runways} IN USE\n"
                atis += (self.metar("CAA") + "\n")
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

            # ICAO Style ATIS
            case "ICAO":
                atis += f"`{self.airport} ATIS {self.get_atis_letter()} {strftime('%H%MZ', gmtime(time()))}\n"
                if self.departure_runways == "":
                    atis += f"DEPARTURES {self.runways}. ARRIVALS {self.runways}\n"
                else:
                    atis += f"DEP RWY {self.departure_runways} ARR RWY {self.runways} IN USE\n"
                approach = self.runways[0:3].upper()
                if approach != "ILS" or approach != "VOR" or approach != "RNV" or approach != "LOC":
                    atis += f"EXP VISUAL APCH\n"
                else:
                    atis += f"EXP {approach} APCH\n"
                self.metar("ICAO")
                atis += f"TEXT PILOTS USE `<#1253808325129408552>` | "
                if self.pdc:
                    atis += f"PDC AVAIL\n"
                else:
                    atis += f"PDC UNAVAIL\n"
                atis += f"SERVER CODE {self.server_code}"
                atis += f"ACKNOWLEDGE INFO {self.get_atis_letter()} ON FIRST CTC WITH APP OR DEL`"
                return atis

# !! There is a lot of string shenanigans going on up there but down here is the real meat and potatoes !!

@discord.app_commands.command(description="Creates a new airport ATIS")
@has_role(RoleIDs.CONTROLLER)
async def generate_atis(ctx: Interaction, airport: str, runways: str, server_code: str, pressure: str,
                        weather_observations: str = "", wind: str = "", temperature: str = "", dewpoint: str = "",
                        clouds: str = "", visibility: str = "", departure_runways: str = "",
                        clearance_station: str = "UNICOM", clearance_frequency: str = "122.800",
                        transition_level: str = "7000", pdc: bool = False):
    
    #Creating the ATIS object
    atis = ATIS(airport, runways, server_code, wind, temperature, dewpoint, pressure, weather_observations, clouds,
                visibility, departure_runways, clearance_station, clearance_frequency, transition_level, pdc, 0, 0)
    
    # Dumping the ATIS object into a pickle file for storage in the database
    try:
        with open(f".atis_database/{airport}.json", "xt") as atis_file:
            await ctx.response.send_message(atis.to_string())
            original_message: discord.InteractionMessage = await ctx.original_response()
            atis.message_id = original_message.id
            json.dump(atis.__dict__, atis_file)
    
    # If an ATIS already exists, the user will be informed
    except FileExistsError:
        await ctx.response.send_message("ATIS already exists for airport, try delete_atis or edit_atis instead",
                                        ephemeral=True)
        return

@discord.app_commands.command(description="Edit an already existing ATIS")
@has_role(RoleIDs.CONTROLLER)
async def edit_atis(ctx: discord.Interaction, airport: str,
                    option: Literal["wind", "temperature", "dewpoint", "pressure", "weather_observations", "clouds",
                                    "visibility", "runways", "departure_runways", "clearance_station",
                                    "clearance_frequency", "pdc_availability", "server_code"],
                    value: str, update_letter: bool=False):
    
    # Loading the ATIS from the database, or informing the user if it does not exist
    try:
        atis_r_file: BufferedReader = open(f".atis_database/{airport}.json", "rb")
        atis: ATIS = ATIS(**json.load(atis_r_file))
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
        print(f"Strange error occured, investigate:\nIn edit_atis in atis.py, expected type not found")
        await ctx.response.send_message("Cannot edit ATIS in this type of channel", ephemeral = True)
        return
    if channel is not None:
        original_atis_partial = channel.get_partial_message(atis.message_id)
        original_atis: Message = cast(Message, await original_atis_partial.fetch())
        # Updaing the original message
        await original_atis.edit(content = atis.to_string())
    else:
        await ctx.response.send_message("Unknown error has occured", ephemeral=True)
        print(f"Strange error occured, investigate:\nIn edit_atis in atis.py, None occured when it shouldn't have")
        return
    
    # Re-opening the ATIS database file and rewritting it with the new information
    try:
        atis_w_file: TextIOWrapper = open(f".atis_database/{airport}.json", "w")
        json.dump(atis.__dict__, atis_w_file)
        atis_w_file.close()
        await ctx.response.send_message(f"ATIS for {airport.upper()} has been edited", ephemeral = True)
    except Exception as e:
        await ctx.response.send_message("An unknown error has occured while writing to the ATIS database",
                                        ephemeral=True)
        print(f"Strange error occured, investigate:\n{e}")
        return

@discord.app_commands.command(description="Delete an already existing ATIS")
@has_role(RoleIDs.CONTROLLER, admin_bypass=True)
async def delete_atis(ctx: discord.Interaction, airport: str):
    
    if os.path.exists(f".atis_database/{airport}.json"):
        try:
            atis_r_file: BufferedReader = open(f".atis_database/{airport}.json", "rb")
            atis: ATIS = ATIS(**json.load(atis_r_file))
            # This could cause an error if run in a strange channel type like a forum, pehaps only allow in atis channel
            original_message: discord.Message = await ctx.channel.fetch_message(atis.message_id) #type: ignore
            await original_message.delete()
            atis_r_file.close()
            os.remove(f".atis_database/{airport.lower()}.json")
            await ctx.response.send_message(f"ATIS for {airport.upper()} has been deleted", ephemeral=True)
        except Exception as e:
            await ctx.response.send_message("An unknown error has occured", ephemeral=True)
            print(f"Strange error occured, investigate:\n{e}")
    else:
        await ctx.response.send_message(f"No ATIS found for {airport.upper()}", ephemeral=True)
# ^!!^ FIX THIS TO MAKE IT MORE ERROR PROOF, TODO ^!!^