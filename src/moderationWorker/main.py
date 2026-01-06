import asyncio
import json
import os
import logging

import aio_pika
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

from ..backend.repositories.ArticleRepository import ArticleRepository
from ..backend.repositories.ApiKeysRepository import ApiKeysRepository
from ..backend.specifications.ApiKeySpecifications import ApiKeySpecification
from ..infrastructure.rabbitmq import publish_notification

from .ReviewService import ReviewService
import requests

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

load_dotenv()

DATABASE_URL = os.getenv("BACKEND_DATABASE_URL")
engine = create_async_engine(DATABASE_URL, future=True)
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

# ------------------ RabbitMQ ------------------
RABBITMQ_URL = os.getenv("RABBITMQ_URL")
QUEUE_NAME = "moderation"

# ------------------ Push service ------------------
Backend_URL = os.getenv("BACKEND_URL")

# ------------------ Message handler ------------------
async def handle_message(data: dict):
    logger.info(f"Получено сообщение: {data}")
    if data.get("event") == "ARTICLE_MODERATE":
        async with AsyncSessionLocal() as db:
            backend_key = await ApiKeysRepository(db).filter_by_spec(ApiKeySpecification.api_is(description="backend"))

            if data.get("requested_by")!= backend_key[0].key:
                logger.info(f"Ошибка: Неверный API ключ для модерации статьи {data['article_id']}.")
                return
            
            article = await ArticleRepository(db).get_by_id(data['article_id'])
            api_key = await ApiKeysRepository(db).filter_by_spec(ApiKeySpecification.api_is(description="moderationWorker"))
            if ReviewService.review(article):
                prev_data = {"event": "ARTICLE_PREVIEW",
                              "article_id": data.get('article_id'),
                                "author_id": data.get('author_id'),
                                "requested_by": api_key[0].key}
                
                await publish_notification(prev_data, queue = "previews")
                logger.info(f"Статья {data.get('article_id')} отправлена на ревью.")
            else:
                api_keys = await ApiKeysRepository(db).filter_by_spec(ApiKeySpecification.api_is(description="moderationWorker"))
                if not api_keys:
                    logger.error("Ключ moderationWorker не найден в базе!")
                    return
                api_key = str(api_keys[0].key).strip()

                url = Backend_URL + f"/articles/{data['article_id']}/reject"
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Token {api_key}"
                }
                logger.info(f"Отправка reject с заголовком: {headers}")
                response = requests.put(url, json=data, headers=headers, timeout=5)

                if response.status_code == 200:
                    logger.info(f"Статья {data['article_id']} отклонена успешно.")
                else:
                    logger.error(f"Ошибка при отклонении статьи {data['article_id']}: {response.status_code} - {response.text}, токен: {api_key}")



# ------------------ RabbitMQ connection ------------------
async def connect_rabbitmq():
    while True:
        try:
            connection = await aio_pika.connect_robust(RABBITMQ_URL)
            logger.info("✅ Подключение к RabbitMQ установлено")
            return connection
        except aio_pika.exceptions.AMQPConnectionError:
            logger.warning("RabbitMQ ещё не готов, повторная попытка через 5 секунд...")
            await asyncio.sleep(5)

async def worker():
    while True:
        try:
            connection = await connect_rabbitmq()
            async with connection:
                channel = await connection.channel()
                await channel.set_qos(prefetch_count=1)
                queue = await channel.declare_queue(QUEUE_NAME, durable=True)
                logger.info(f"🚀 Worker запущен и слушает очередь '{QUEUE_NAME}'")

                async with queue.iterator() as queue_iter:
                    async for message in queue_iter:
                        async with message.process():
                            try:
                                data = json.loads(message.body.decode())
                                await handle_message(data)
                            except Exception as e:
                                logger.error(f"Ошибка обработки сообщения: {e}")
        except aio_pika.exceptions.AMQPConnectionError:
            logger.warning("Потеряно соединение с RabbitMQ, переподключаемся через 5 секунд...")
            await asyncio.sleep(5)
        except Exception as e:
            logger.error(f"Непредвиденная ошибка воркера: {e}")
            await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(worker())
