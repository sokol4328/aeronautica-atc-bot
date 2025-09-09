import time
from random import randint
from typing import List
import discord
from discord import message

class ATIS:
    def __init__(self, airport: str, wind: str, temp: str, dewpoint: str, pressure: str, clouds: str, visibility: str, dispatch_station: str, dispatch_frequency: str, runway: str, dep_runway: str):
        self.airport: str = airport.upper()
        self.atis_letter: int = 0
        self.fir: str = get_fir(self.airport)
        self.wind: str = wind
        self.temp: str = temp
        self.dewpoint: str = dewpoint
        self.pressure: str = pressure
        self.clouds: str = clouds
        self.visibility: str = visibility
        self.runway: str
        self.approach: str
        if runway.upper()[0:3] == "ILS" or runway.upper()[0:3] == "LOC" or runway.upper()[0:3] == "VOR":
            self.runways = runway[4:]
            self.approach = runway.upper()[0:3]
        else:
            self.runway = runway
            self.approach = "VISUAL"
        self.dep_runway: str = dep_runway
        self.dispatch_station: str = "UNICOM"
        self.dispatch_freq: str = "122.800"
        self.pdc: str = "UNAVAIL"
        self.server_code: str = "000000"
        self.channel: int
        self.message: int

    @staticmethod
    def get_info_letter(info_num: int):
        return chr(ord('a') + info_num).upper()
    
    def edit_atis(self, option: str, value: str):
        match option:
            case "wind":
                self.wind = value
            case "temperature":
                self.temp = value
            case "dewpoint":
                self.dewpoint = value
            case "pressure":
                self.pressure = value
            case "clouds":
                self.clouds = value
            case "visibility":
                self.visibility = value
            case "runway":
                if value.upper()[0:3] == "ILS" or value.upper()[0:3] == "LOC" or value.upper()[0:3] == "VOR":
                    self.runways = value[4:]
                    self.approach = value.upper()[0:3]
                else:
                    self.runway = value
                    self.approach = "VISUAL"
            case "depature_runway":
                self.dep_runway = value
            case "dispatch_station":
                self.dispatch_station = value
            case "dispatch_frequency":
                self.dispatch_freq = value
            case "pdc_availability":
                self.pdc = value
            case "server_code":
                self.server_code = value
    
    def to_string(self) -> str:
        if self.fir == "FAA":
            atis: str = "`"
            atis += f"{self.airport} ATIS INFO {ATIS.get_info_letter(self.atis_letter)} {get_time_utc()}"
            atis += f"\n{self.wind}KT {self.visibility}SM {self.clouds} {self.temp}/{self.dewpoint} A{self.pressure}"
            atis += f"\n{self.approach} APCH RWY {self.runway}"
            if len(self.dep_runway) != 0:
                f"\nDEP {self.dep_runway}"
            atis += f"\nREADBACK ALL RUNWAY HOLD SHORT INSTRUCTIONS"
            atis += f"\nCONTACT {self.dispatch_station} ON {self.dispatch_freq} FOR CLNC INSTRUCTIONS"
            atis += f"\nTEXT PILOTS USE `<#1253808325129408552>` | PDC {self.pdc}"
            atis += f"\nADVIS YOU HAVE {ATIS.get_info_letter(self.atis_letter)}`"
            return atis
        elif self.fir == "CAA":
            return "WIP"
        elif self.fir == "ICAO":
            return "WIP"
        else:
            return "Error"
        
class LOA:
    def __init__(self, staff_member: int, reason: str):
        self.staff_member = staff_member
        self.reason = reason

def find_frequency(airport: str) -> str:
    return f"{airport.upper()} WIP"
    
def get_time_utc() -> str:
    return time.strftime("%H%MZ", time.gmtime(time.time()))

def generate_squawk() -> str:
    squawk: str = ""
    for i in range(0,4):
        squawk = squawk + str(randint(0,7))
    return squawk

# TODO
def get_fir(airport: str):
    return "FAA"