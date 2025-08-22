from aiogram import Router, F, Bot
from aiogram.types import Message, FSInputFile
from utils.plot_service import plotpricechart
from pathlib import Path
from keyboards import charts_keyboard
from datetime import datetime


router = Router()


@router.message(F.text.startswith('/charts'))
async def charts(message: Message,bot:Bot):
    parts = message.text.strip().split()
    if len(parts) < 2:
        await message.reply("Укажите ID монеты /charts bitcoin", reply_markup=charts_keyboard.keyboard)
        return None
    coin_id = parts[1].lower().strip()
    await bot.send_chat_action(chat_id=message.chat.id, action="upload_photo")
    chart_path = plotpricechart(coin_id)
    if chart_path and chart_path.exists():
        photo = FSInputFile(chart_path)
        await message.answer_photo(photo, caption=f"График {coin_id} {datetime.now()}")
    else:
        await message.answer(text="Не удалось посторить график")