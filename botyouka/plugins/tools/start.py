from pyrogram import *
import asyncio

@Client.on_message(filters.command('start', prefixes=['/', ',', '.', '!', '$', '-', '}', '{', ']','[', '(', ')', '#', '%' ], case_sensitive=False) & filters.text)
async def start(client, message):
    m1 = await client.send_message(chat_id=message.chat.id, text=f"<b><i>Compa @{message.from_user.username} Esperese alv estoy \nObteniendo Permisos... ✅</i></b>", reply_to_message_id=message.id)
    await asyncio.sleep(1.5)
    await m1.edit(text=f"<b>Bienvenido @{message.from_user.username} a Sokka CHK 「♚」 Usa /register para ingresar en nuestra database</b>")