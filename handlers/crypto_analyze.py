from aiogram import Router, F
from aiogram.types import Message
from utils.coingeeko_service import get_current_price

router = Router()


@router.message(F.text.startswith('/analyze'))
async def analyze(message: Message):
    parts = message.text.strip().split()
    if len(parts) < 2:
        await message.reply("Укажите ID монеты /analyze bitcoin")
        return
    coin_id = parts[1].lower().strip()
    price = get_current_price(coin_id)
    if price is None:
        await message.reply("Укажите верный ID")
        return
    response = f'Текущая цена {coin_id.capitalize()}: {price}'
    await message.reply(response)
