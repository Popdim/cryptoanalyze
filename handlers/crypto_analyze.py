from aiogram import Router, F
from aiogram.types import Message
from utils.coingeeko_service import get_current_price, get_daily_summary

router = Router()


@router.message(F.text.startswith('/price'))
async def price(message: Message):
    parts = message.text.strip().split()
    if len(parts) < 2:
        await message.reply("Укажите ID монеты /price bitcoin")
        return
    coin_id = parts[1].lower().strip()
    price = get_current_price(coin_id)
    if price is None:
        await message.reply("Укажите верный ID")
        return
    response = f'Текущая цена {coin_id.capitalize()}: {price}'
    await message.reply(response)

@router.message(F.text.startswith('/analyze'))
async def analyze(message: Message):
    parts = message.text.strip().split()
    if len(parts) < 2:
        await message.reply("Укажите ID монеты /analyze bitcoin")
        return None
    coin_id = parts[1].lower().strip()
    summary = get_daily_summary(coin_id)
    if summary is None:
        await message.reply("No data found")
        return
    text = f"""💸{coin_id.capitalize()} за последние 24 часа:
    цена: *{summary["current_price"]:.2f} USD*
    минимальная цена: *{summary["min_price"]:.2f} USD*
    максимальная цена: *{summary["max_price"]:.2f} USD*
    объем: *{summary["total_volume"]:.2f}*"""
    await message.reply(text, parse_mode="Markdown")
