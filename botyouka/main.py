import logging
from os import name as os_name, system as os_system
from huepy import bold, green
from functions.variables import API_ID, API_HASH, BOT_TOKEN, NAME_BOT
from pyrogram import Client
from pyrogram.enums import ParseMode

# CLEAR CONSOLE
if os_name == "nt": os_system("cls") 
else: os_system("clear")

# LOGS
logging.basicConfig(level=logging.INFO)

# CONFIGURE CLIENT
bot = Client(
    NAME_BOT,
    api_id =  API_ID,
    api_hash = API_HASH,
    bot_token = BOT_TOKEN,
    plugins = dict(root="plugins"),
    parse_mode=ParseMode.HTML
)

# START CLIENTS
print(bold(green(f"youka botsito{NAME_BOT}")))
bot.run()