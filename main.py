from aiogram import Bot, Dispatcher
import config
from handlers import common, crypto_analyze, crypto_charts
import asyncio


async def main():
    bot = Bot(token=config.TOKEN_TG)
    dp = Dispatcher()
    dp.include_router(common.router)
    dp.include_router(crypto_analyze.router)
    dp.include_router(crypto_charts.router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
