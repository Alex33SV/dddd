from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from functions.variables import PREFIXES
from gateways.lp2 import payeezy, CaptchaSolver
import time

keyboard = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("Buy 💰", url="https://t.me/Youka503"),
    ]
])

@Client.on_message(filters.command('lp', PREFIXES))
async def gate_lp(client, message):
    start_time = time.time()
    card_info = message.text.split()

    if len(card_info) < 2:
        await message.reply("<b>Please Enter The Card Details! ⚠️</b>", quote=True)
        return
    
    card_details = card_info[1].split('|')
    
    if len(card_details) != 4:
        await message.reply("<b>Please Enter The Complete Card Details! ⚠️</b>", quote=True)
        return

    cc, mes, ano, cvv = card_details
    card = f"{cc}|{mes}|{ano}|{cvv}"
    
    msgedit = await client.send_message(chat_id=message.chat.id, text=f"""
<b>Gateway: PAYEEZY 20USD</b> (/lp) 
<b>Card: <code>{card}</code></b>
<b>Processing Please Wait...</b>""", reply_to_message_id=message.id)
         
    msg, avs, bank_message, status = await payeezy(cc, mes, ano, cvv)  # Utiliza la función payeezy para el procesamiento
    taken = round(time.time() - start_time, 2)
        
    await msgedit.edit_text(text=f"""
<b>
Card: <code>{card}</code>
Status: <code>{status}</code>
Response: <code>{msg} - {bank_message}</code>
Avs Response: <code>{avs}</code>
Gateway: PAYEEZY 20USD
Time: <code>{taken}</code>
</b>
""", reply_markup=keyboard)
