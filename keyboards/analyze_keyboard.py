from aiogram import types

button_btc = types.KeyboardButton(text='/analyze bitcoin')
button_eth = types.KeyboardButton(text='/analyze ethereum')
button_ton = types.KeyboardButton(text='/analyze the-open-network')
button_xrp = types.KeyboardButton(text='/analyze ripple')
button_sol = types.KeyboardButton(text='/analyze solana')
kb = [
    [button_btc, button_eth, button_ton],
    [button_xrp, button_sol]
]
keyboard=types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)