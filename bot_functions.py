import time
from random import randint
from typing import List

class ATIS:
    def __init__(self, airport: str, wind: str, temp: str, dewpoint: str, pressure: str, clouds: str, visibility: str):
        self.airport: str = airport.upper()
        self.atis_letter: int = 0
        self.fir: str = get_fir(self.airport)
        self.wind: str = wind
        self.temp: str = temp
        self.dewpoint: str = dewpoint
        self.pressure: str = pressure
        self.clouds: str = clouds
        self.visibility: str = visibility
        self.approach: str = "VISUAL"
        self.runways: List[str] = []
        self.dep_runways: List[str] = []
        self.dispatch_station: str = "UNICOM"
        self.dispatch_freq: str = "122.800"
        self.pdc: str = "UNAVAIL"
        self.server_code: str = "000000"

    @staticmethod
    def get_info_letter(info_num: int):
        return chr(ord('a') + info_num).upper()
    
    def to_string(self):
        if self.fir == "FAA":
            atis: str = "`"
            atis += f"{self.airport} ATIS INFO {ATIS.get_info_letter(self.atis_letter)} {get_time_utc()}"
            atis += f"\n{self.wind}KT {self.visibility}SM {self.clouds} {self.temp}/{self.dewpoint} A{self.pressure}"
            atis += f"\n{self.approach} APCH "
            for runway in self.runways:
                atis += f"{runway} "
            if len(self.dep_runways) != 0:
                f"\nDEP "
                for runway in self.dep_runways:
                    atis += f"{runway} "
            atis += f"\nREADBACK ALL RUNWAY HOLD SHORT INSTRUCTIONS"
            atis += f"\nCONTACT {self.dispatch_station} ON {self.dispatch_freq} FOR CLNC INSTRUCTIONS"
            atis += f"\nTEXT PILOTS USE `<#1253808325129408552>` | PDC {self.pdc}"
            atis += f"\nADVIS YOU HAVE {ATIS.get_info_letter(self.atis_letter)}`"
            return atis
        elif self.fir == "CAA":
            pass
        elif self.fir == "ICAO":
            pass

def find_frequency(airport: str) -> str:
    if airport.upper() == "KCIA":
        return "KCIA WIP"
    else:
        return "WIP"
    
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