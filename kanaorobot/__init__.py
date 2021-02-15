import logging
import time
from telegraph import Telegraph
from kanaorobot.config import Config
from pyrogram import Client, filters, errors
from jikanpy import Jikan
StartTime = time.time()
logging.basicConfig(level=logging.INFO)

telegraph = Telegraph()
telegraph.create_account(short_name='kanao')

API_ID = Config.API_ID
API_HASH = Config.API_HASH
BOT_TOKEN = Config.BOT_TOKEN
DB_URI = Config.DB_URI
ALLOWED_USERS = [
        942202199
    ]
LOG_CHANNEL = Config.LOG_CHANNEL

jikan = Jikan()
KANAO = Client("Kanao", api_id = API_ID, api_hash = API_HASH, bot_token = BOT_TOKEN)
