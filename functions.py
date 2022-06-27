from telethon import TelegramClient, events, Button
from telethon.tl.types import PeerChannel

approval_keyboard = [
    [
        Button.inline("Approve", b"approved"),
        Button.inline("Reject", b"rejected")
    ]
]

approved_keyboard = [
    [
        Button.inline("Delete", b"delete")
    ]
]

rejected_keyboard = [
    [
        Button.inline("Undo", b"undo")
    ]
]


async def client_forward(client: TelegramClient, bot_username: str, client_black_list: list):
    @client.on(events.NewMessage(chats=client_black_list, blacklist_chats=True, incoming=True))
    async def forward_message(event):
        if isinstance(event.message.peer_id, PeerChannel):  # forward only channel messages to bot
            print(event.stringify(), "\n Client Forward")
            await client.send_message(bot_username, event.message)


async def bot_forward(bot: TelegramClient, backend: int, bot_allowed_list: list):
    @bot.on(events.NewMessage(chats=bot_allowed_list))
    async def forward_message(event):
        print(event.stringify(), "\n Bot Forward")
        await bot.send_message(entity=backend, message=event.message, buttons=approval_keyboard)


async def bot_callback(bot: TelegramClient, deals_channel, backend):
    @bot.on(events.CallbackQuery(chats=backend))
    async def callback_handler(event):
        print(event.stringify(), "\n Bot CallBack")
        message = await event.get_message()
        print(message)
        if event.data == b'approved':
            print("Approved")
            await bot.send_message(entity=deals_channel, message=message.message)
            await bot.edit_message(entity=backend, message=message.id, buttons=approved_keyboard)
        elif event.data == b'rejected':
            print("Rejected")
            await bot.edit_message(entity=backend, message=message.id, buttons=rejected_keyboard)
        elif event.data == b'delete':
            print("Deleted")
            await bot.delete_messages(entity=backend, message_ids=message.id)
        else:
            print("Re-Publishing")
            await bot.send_message(entity=backend, message=message, buttons=approval_keyboard)
            await bot.edit_message(entity=backend, message=message.id)
