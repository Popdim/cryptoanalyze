from aiogram import types

button_btc = types.KeyboardButton(text='/ai bitcoin')
button_eth = types.KeyboardButton(text='/ai ethereum')
button_ton = types.KeyboardButton(text='/ai the-open-network')
button_xrp = types.KeyboardButton(text='/ai ripple')
button_sol = types.KeyboardButton(text='/ai solana')
kb = [
    [button_btc, button_eth, button_ton],
    [button_xrp, button_sol]
]
keyboard=types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)