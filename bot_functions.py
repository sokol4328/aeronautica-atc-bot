import time

def find_frequency(airport: str) -> str:
    if airport.upper() == "KCIA":
        return "KCIA WIP"
    else:
        return "WIP"
    
def get_time_utc() -> str:
    return time.strftime("%H%MZ", time.gmtime(time.time()))