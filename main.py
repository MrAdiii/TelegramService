from telethon import TelegramClient
from telethon.tl.types import PeerChannel, PeerUser

from functions import client_forward, bot_forward, bot_callback
import os

api_id = int(os.environ['API_ID'])
api_hash = os.environ['API_HASH']
bot_token = os.environ['BOT_TOKEN']

bot_username = os.environ['BOT_USERNAME']
backend = int(os.environ['BACKEND'])
user_id = PeerUser(int(os.environ['USER_ID']))
deals_channel = PeerChannel(int(os.environ['DEALS_CHANNEL']))
client_black_list = [backend, deals_channel]
bot_allowed_list = [backend, user_id]

client = TelegramClient('anon', api_id, api_hash)
bot = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

with client:
    client.loop.create_task(client_forward(client, bot_username, client_black_list))
    client.loop.create_task(bot_forward(bot, backend, bot_allowed_list))
    client.loop.create_task(bot_callback(bot, deals_channel, backend))
    client.loop.run_forever()
