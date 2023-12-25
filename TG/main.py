import asyncio
import logging

from aiogram import Bot
from aiogram.enums.parse_mode import ParseMode

import config
from DATABASE.db import async_db_session
from TG.sheduler import sheduler
from handlers import router, dp


bot = Bot(token=config.BOT_TOKEN, parse_mode=ParseMode.HTML)


async def bot_start():
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


async def main():
    await async_db_session.init()
    await asyncio.gather(sheduler(), bot_start())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
