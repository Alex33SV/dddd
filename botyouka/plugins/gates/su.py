from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from functions.variables import PREFIXES
from gateways.su2 import payeezy, CaptchaSolver
import time

keyboard = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("Buy 💰", url="https://t.me/Youka503"),
    ]
])

@Client.on_message(filters.command('su', PREFIXES))
async def gate_an(client, message):
    start_time = time.time()
    card_info = message.text.split()[1]  
    card_details = card_info.split('|')  
    if len(card_details) != 4:
        await message.reply("<b>Please Enter All Card Details in the correct format! ⚠️</b>", quote=True)
        return

    cc, mes, ano, cvv = card_details[0], card_details[1], card_details[2], card_details[3]

    if not is_luhn_valid(cc):
        await message.reply("<b>Invalid Card Number! ⚠️</b>", quote=True)
        return
    
    card = f"{cc}|{mes}|{ano}|{cvv}"
    
    msgedit = await client.send_message(chat_id=message.chat.id, text=f"""
<b>Gateway: Payeezy 20$</b> (/su) 
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
Gateway: Payeezy 20$
Time: <code>{taken}</code>
</b>
""", reply_markup=keyboard)

@staticmethod
def is_luhn_valid(cc: str) -> bool:
    assert isinstance(cc, str), "The cc must be an instance of str"
    num = list(map(int, str(cc)))
    return sum(num[::-2] + [sum(divmod(d * 2, 10)) for d in num[-2::-2]]) % 10 == 0