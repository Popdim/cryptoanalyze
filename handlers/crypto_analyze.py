from aiogram import Router, F, Bot
from aiogram.types import Message
from utils.coingeeko_service import get_current_price, get_daily_summary, get_historical_data
from utils.indicators import get_rsi, get_ema, simple_signal, get_macd, macd_signal
from utils.text_template import make_ai_prompt
from utils.openai_service import get_ai_prediction
from keyboards import analyze_keyboard, price_keyboard, ai_keyboard

router = Router()


@router.message(F.text.startswith('/price'))
async def price(message: Message):
    parts = message.text.strip().split()
    if len(parts) < 2:
        await message.reply("Укажите ID монеты /price bitcoin", reply_markup=price_keyboard.keyboard)
        return None
    coin_id = parts[1].lower().strip()
    price = get_current_price(coin_id)
    if price is None:
        await message.reply("Укажите верный ID")
        return
    response = f'Текущая цена {coin_id.capitalize()}: {price}'
    await message.reply(response)


@router.message(F.text.startswith('/analyze'))
async def analyze(message: Message, bot: Bot):
    parts = message.text.strip().split()
    if len(parts) < 2:
        await message.reply("Укажите ID монеты /analyze bitcoin", reply_markup=analyze_keyboard.keyboard)
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
    macd_data = get_macd(df, fast_period=14, slow_period=30, signal_period=9)
    if len(df) > 1:
        prev_macd_data = get_macd(df.iloc[:-1], fast_period=14, slow_period=30, signal_period=9)
        macd_sig = macd_signal(macd_data["macd_line"], macd_data["signal_line"], macd_data["histogram"],
                               prev_macd_data["histogram"])
    else:
        macd_sig = macd_signal(macd_data["macd_line"], macd_data["signal_line"], macd_data["histogram"])
    text = f"""💸{coin_id.capitalize()} за последние 24 часа:
    цена: *{summary["current_price"]:.2f} USD*
    минимальная цена: *{summary["min_price"]:.2f} USD*
    максимальная цена: *{summary["max_price"]:.2f} USD*
    объем: *{summary["total_volume"]:.2f}*
    RSI=*{current_rsi}*
    рекомендация по RSI:*{signal_rsi}*
    EMA=*{current_ema}*
    MACD=*{macd_data["macd_line"]}*
    сигнал по MACD:*{macd_data["signal_line"]}*
    рекомендация по MACD:*{macd_sig}*
    гистограма:*{macd_data["histogram"]}*
"""
    await message.reply(text, parse_mode="Markdown")
    # await bot.send_chat_action(chat_id=message.chat.id, action="typing")
    # prompt = make_ai_prompt(coin_id, summary, current_rsi, current_ema, signal_rsi)
    # answer = await get_ai_prediction(prompt)
    # await message.reply(answer, parse_mode="Markdown")


@router.message(F.text.startswith('/ai'))
async def ai(message: Message, bot: Bot):
    parts = message.text.strip().split()
    if len(parts) < 2:
        await message.reply("Укажите ID монеты", reply_markup=ai_keyboard.keyboard)
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
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")
    prompt = make_ai_prompt(coin_id, summary, current_rsi, current_ema, signal_rsi)
    answer = await get_ai_prediction(prompt)
    await message.reply(answer, parse_mode="Markdown")
