import time
from random import randint

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

def generate_atis() -> str:
    atis: str = ""

    atis = atis + "`test`"

    return atis