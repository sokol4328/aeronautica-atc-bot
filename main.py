from bot import AeroATCBot
import logging
from dotenv import load_dotenv
import os
import json

with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

LOG_LEVEL = config["logging"]["level"]
LOG_FILE = config["logging"]["log_file"]

load_dotenv()
TOKEN: str = os.environ["DISCORD_TOKEN"]

handler = logging.FileHandler(filename=LOG_FILE, encoding='utf-8', mode='w')

if __name__ == "__main__":
    bot = AeroATCBot()
    bot.run(TOKEN, log_handler=handler, log_level=logging.getLevelName(LOG_LEVEL))