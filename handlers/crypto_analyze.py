from aiogram import Router, F
from aiogram.types import Message
from utils.coingeeko_service import get_current_price, get_daily_summary, get_historical_data
from utils.indicators import get_rsi, get_ema, simple_signal

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
    df = get_historical_data(coin_id, days=30)
    current_rsi = get_rsi(df, period=30)
    current_ema = get_ema(df, period=30)
    signal_rsi = simple_signal(rsi=current_rsi)
    text = f"""💸{coin_id.capitalize()} за последние 24 часа:
    цена: *{summary["current_price"]:.2f} USD*
    минимальная цена: *{summary["min_price"]:.2f} USD*
    максимальная цена: *{summary["max_price"]:.2f} USD*
    объем: *{summary["total_volume"]:.2f}*
    RSI=*{current_rsi}*
    рекомендация по RSI:*{signal_rsi}*
    EMA=*{current_ema}*"""
    await message.reply(text, parse_mode="Markdown")
