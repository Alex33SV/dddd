import random
import time
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests

last_command_time = {}

ANTISPAM_TIME = 10

def generate_ccv(card_type):
    if card_type.lower() == "american express":
        return str(random.randint(1000, 9999))
    else:
        return str(random.randint(100, 999))

def complete_card_number(bin_number, card_type):
    if card_type.lower() == "american express":
        remaining_digits = 15 - len(bin_number)
    else:
        remaining_digits = 16 - len(bin_number)
    
    incomplete_number = bin_number + "".join([str(random.randint(0, 9)) for _ in range(remaining_digits - 1)])
    return incomplete_number + calculate_luhn_check_digit(incomplete_number)

def calculate_luhn_check_digit(number):
    digits = [int(d) for d in number]
    for i in range(len(digits) - 1, -1, -2):
        digits[i] *= 2
        if digits[i] > 9:
            digits[i] -= 9
    total_sum = sum(digits)
    return str((10 - (total_sum % 10)) % 10)


def country_code_to_flag(country_code):

    country_code = country_code.upper()
    
    return chr(ord(country_code[0]) + 127397) + chr(ord(country_code[1]) + 127397)

def get_bin_info(bin_number):
    try:
        url = f"https://lookup.binlist.net/{bin_number}"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            return {
                "vendor": data.get("scheme", "Unknown").capitalize(),
                "type": data.get("type", "Unknown").capitalize(),
                "level": data.get("brand", "Unknown").capitalize(),
                "country": data.get("country", {}).get("name", "Unknown").upper(),
                "country_code": data.get("country", {}).get("alpha2", ""),
                "bank": data.get("bank", {}).get("name", "Unknown").upper()
            }
        else:
            return None
    except Exception as e:
        print(f"Error al obtener información del BIN: {e}")
        return None

def generate_cards(bin_number, exp_date, card_type, quantity=10):
    cards = []
    for _ in range(quantity):
        full_number = complete_card_number(bin_number, card_type)
        ccv = generate_ccv(card_type)
        card = f"{full_number}|{exp_date}|{ccv}"
        cards.append(card)
    return cards

def format_response(bin_number, exp_date, cards, bin_info):
    response = f"💳 **Extra:** {bin_number}|{exp_date}|rnd\n\n"
    response += "╔═[💳]════════════════════════════╗\n"
    
    for card in cards:
        response += f"<code>{card}</code>\n"
    
    response += "╚════════════════════════════════╝\n\n"
    
    if bin_info:
        country_code = bin_info.get('country_code', '')
        
        flag_emoji = country_code_to_flag(country_code) if country_code else "❓"
        
        response += f"{flag_emoji} ╚Country:╝ {bin_info['country']}\n"
        response += f"💳 ╚Vendor:╝ {bin_info['vendor']}\n"
        response += f"📇 ╚Type:╝ {bin_info['type']}\n"
        response += f"🛡️ ╚Level:╝ {bin_info['level']}\n"
        response += f"🏦 ╚Bank:╝ {bin_info['bank']}\n"
    else:
        response += "❌ **No se pudo obtener información completa del BIN ingresado.**\n"
    
    response += "\n└Bot by » [@YouKa503]\n"
    
    return response

@Client.on_message(filters.command("gen", prefixes="."))
async def generate(client, message):
    user_id = message.from_user.id
    current_time = time.time()

    if user_id in last_command_time and (current_time - last_command_time[user_id]) < ANTISPAM_TIME:
        remaining_time = ANTISPAM_TIME - (current_time - last_command_time[user_id])
        await message.reply(f"⏳ Por favor espera {int(remaining_time)} segundos antes de usar este comando nuevamente.")
        return

    last_command_time[user_id] = current_time

    try:
        if "|" in message.text:
            _, bin_data = message.text.split(" ", 1)
            bin_number, exp_month, exp_year = bin_data.split("|")
        else:
            _, bin_number, exp_month, exp_year = message.text.split()

        exp_date = f"{exp_month}|{exp_year}"
    except ValueError:
        await message.reply("Formato incorrecto. Usa: `.gen BIN MM YY` o `.gen BIN|MM|YYYY`")
        return
    
    bin_info = get_bin_info(bin_number[:6])
    
    card_type = bin_info['vendor'] if bin_info else "Desconocido"
    cards = generate_cards(bin_number, exp_date, card_type)
    response = format_response(bin_number, exp_date, cards, bin_info)
    
    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("Re Gen 🔄", callback_data=f"regen:{bin_number}:{exp_month}:{exp_year}")]]
    )
    
    await message.reply(response, reply_markup=keyboard)

@Client.on_callback_query(filters.regex(r"regen"))
async def handle_regen(client, callback_query):
    user_id = callback_query.from_user.id
    current_time = time.time()

    if user_id in last_command_time and (current_time - last_command_time[user_id]) < ANTISPAM_TIME:
        remaining_time = ANTISPAM_TIME - (current_time - last_command_time[user_id])
        await callback_query.answer(f"⏳ Por favor espera {int(remaining_time)} segundos antes de usar este comando nuevamente.", show_alert=True)
        return

    last_command_time[user_id] = current_time

    _, bin_number, exp_month, exp_year = callback_query.data.split(":")
    exp_date = f"{exp_month}|{exp_year}"
    
    bin_info = get_bin_info(bin_number[:6])
    
    card_type = bin_info['vendor'] if bin_info else "Desconocido"
    cards = generate_cards(bin_number, exp_date, card_type)
    response = format_response(bin_number, exp_date, cards, bin_info)
    
    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("Re Gen 🔄", callback_data=f"regen:{bin_number}:{exp_month}:{exp_year}")]]
    )
    
    await callback_query.message.edit_text(response, reply_markup=keyboard)
