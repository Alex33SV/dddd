from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from functions.variables import PREFIXES
from gateways.pyz2 import payeezy
import time

keyboard = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("Buy 💰", url="https://t.me/Youka503"),
    ]
])

last_command_time_su = {}

ANTISPAM_TIME = 25

@Client.on_message(filters.command('pyz', PREFIXES))
async def gate_an(client, message):
    user_id = message.from_user.id
    current_time = time.time()

    if user_id in last_command_time_su:
        elapsed_time = current_time - last_command_time_su[user_id]
        if elapsed_time < ANTISPAM_TIME:
            remaining_time = ANTISPAM_TIME - elapsed_time
            await message.reply(f"⏳ Por favor espera {int(remaining_time)} segundos antes de usar este comando nuevamente.")
            return

    last_command_time_su[user_id] = current_time

    start_time = time.time()
    
    card_info = message.text.split()[1].split("|")
    
    if len(card_info) != 4: 
        await message.reply("<b>Please Enter The Card Details! ⚠️</b>", quote=True)
        return

    cc, mes, ano, cvv = card_info[0], card_info[1], card_info[2], card_info[3]
    card = f"{cc}|{mes}|{ano}|{cvv}"
    
    msgedit = await client.send_message(chat_id=message.chat.id, text=f"""
<b>Gateway: Payeezy 200$</b> (/pyz) 
<b>Card: <code>{card}</code></b>
<b>Processing Please Wait...</b>""", reply_to_message_id=message.id)
         
    msg, avs, bank_message, status = await payeezy(cc, mes, ano, cvv)
    taken = round(time.time() - start_time, 2)
        
    await msgedit.edit_text(text=f"""
<b>
Card: <code>{card}</code>
Status: <code>{status}</code>
Response: <code>{msg} - {bank_message}</code>
Avs Response: <code>{avs}</code>
Gateway: Payeezy avs 200$
Time: <code>{taken}</code>
</b>
""", reply_markup=keyboard)

