import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()
import asyncio
import logging
from tg.utils import invoice_checker
from aiogram import Bot, Dispatcher
from aiogram.filters import BaseFilter
from aiogram.types import Message




async def main():
    from aiogram.fsm.storage.memory import MemoryStorage
    from tg.handlers.changer import router
    bot = Bot(token="7642412235:AAHAo4aRacdPx5HxT0SdMUhaq-L12AbALS0")
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_routers(router)
    await bot.delete_webhook(drop_pending_updates=True)
    asyncio.create_task(invoice_checker(bot))
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())