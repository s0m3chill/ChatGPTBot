import logging

from core import bot, dp, DataStorage
from config import WEBHOOK_URL
from config import WEBHOOK_PATH
from config import WEBAPP_HOST
from config import WEBAPP_PORT
from aiogram import executor, Dispatcher
from aiogram.utils.executor import start_webhook
from app.handlers.common import register_handlers_common
from app.handlers.questions import register_handlers_questions
from app.handlers.payments import register_handlers_payments

logger = logging.getLogger(__name__)

async def on_startup(dispatcher: Dispatcher) -> None:
    await DataStorage.connect()
    await bot.delete_webhook()
    logger.info("Before setting hook")
    await bot.set_webhook(WEBHOOK_URL) # drop_pending_updates=True
    logger.info("After setting hook")
    logger.info(await bot.get_webhook_info())

async def on_shutdown(dispatcher: Dispatcher) -> None:
    await DataStorage.disconnect()
    await dp.storage.close()
    await dp.storage.wait_closed()
    await bot.session.close()
    await bot.delete_webhook()

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")

    register_handlers_common(dp)
    register_handlers_questions(dp)
    register_handlers_payments(dp)

if __name__ == '__main__':
    try:
        logger.info("Before starting hook")
        start_webhook(
            dispatcher=dp,
            webhook_path=WEBHOOK_PATH,
            skip_updates=True,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            host=WEBAPP_HOST,
            port=WEBAPP_PORT,
        )
        logger.info("After starting hook")
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")