import logging
import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")


async def delete_service_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Удаляет системное сообщение о входе/выходе участника из группы."""
    try:
        await update.message.delete()
        logger.info("Системное сообщение удалено")
    except Exception as e:
        logger.warning(f"Не получилось удалить сообщение: {e}")


def main():
    if not BOT_TOKEN:
        raise SystemExit("Не найден BOT_TOKEN — проверь файл .env")

    app = Application.builder().token(BOT_TOKEN).build()

    # Ловим оба типа системных сообщений: вход в группу и выход из неё
    app.add_handler(
        MessageHandler(
            filters.StatusUpdate.NEW_CHAT_MEMBERS | filters.StatusUpdate.LEFT_CHAT_MEMBER,
            delete_service_message,
        )
    )

    logger.info("Бот запущен и ждёт события в группах...")
    app.run_polling()


if __name__ == "__main__":
    main()