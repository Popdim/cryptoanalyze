from aiogram import types

button_start = types.KeyboardButton(text='/start')
button_help = types.KeyboardButton(text='/help')
button_info = types.KeyboardButton(text='/info')
button_analyze = types.KeyboardButton(text='/analyze')
button_price = types.KeyboardButton(text='/price')
button_ai = types.KeyboardButton(text='/ai')
kb = [
    [button_start, button_help, button_info],
    [button_analyze, button_price, button_ai]
]
keyboard=types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)