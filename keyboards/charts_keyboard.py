from aiogram import types

button_btc = types.KeyboardButton(text='/charts bitcoin')
button_eth = types.KeyboardButton(text='/charts ethereum')
button_ton = types.KeyboardButton(text='/charts the-open-network')
button_xrp = types.KeyboardButton(text='/charts ripple')
button_sol = types.KeyboardButton(text='/charts solana')
kb = [
    [button_btc, button_eth, button_ton],
    [button_xrp, button_sol]
]
keyboard=types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)