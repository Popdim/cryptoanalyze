from aiogram import types

button_btc = types.KeyboardButton(text='/price bitcoin')
button_eth = types.KeyboardButton(text='/price ethereum')
button_ton = types.KeyboardButton(text='/price the-open-network')
button_xrp = types.KeyboardButton(text='/price ripple')
button_sol = types.KeyboardButton(text='/price solana')
kb = [
    [button_btc, button_eth, button_ton],
    [button_xrp, button_sol]
]
keyboard=types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)