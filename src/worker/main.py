import asyncio
import json
import os
import logging

import aio_pika
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

from ..usersApi.repositories.UserRepository import UserRepository
from ..usersApi.repositories.SubscriptionsRepository import SubscriptionRepository
from ..usersApi.specifications.SubscriptionSpecifications import SubscriptionSpecification
from ..usersApi.specifications.UserSpecifications import UserSpecification
import httpx

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

load_dotenv()

# ------------------ Database ------------------
DATABASE_URL = os.getenv("USERS_DATABASE_URL")
engine = create_async_engine(DATABASE_URL, future=True)
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

# ------------------ RabbitMQ ------------------
RABBITMQ_URL = os.getenv("RABBITMQ_URL")
QUEUE_NAME = "notifications"

# ------------------ Push service ------------------
PUSH_URL = os.getenv("PUSH_URL")

async def send_push(token: str, message: str):
    payload = {"message": message}
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    logger.info(f"Отправка push пользователю {token}: {message}")

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(PUSH_URL, headers=headers, json=payload, timeout=5.0)
            response.raise_for_status()
            logger.info(f"Push успешно отправлен. Статус: {response.status_code}")
        except httpx.RequestError as e:
            logger.error(f"Ошибка при отправке запроса: {e}")
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP ошибка: {e.response.status_code} - {e.response.text}")

# ------------------ Message handler ------------------
async def handle_message(data: dict):
    logger.info(f"Получено сообщение: {data}")
    if data.get("event") == "ARTICLE_CREATED":
        message = f"Пользователь {data['author_id']} выпустил новый пост: {data['article_id']}"
        async with AsyncSessionLocal() as db:
            subscribers = await SubscriptionRepository(db).filter_by_spec(
                SubscriptionSpecification.target_user_id_is(data['author_id'])
            )
            logger.info(f"Найдено {len(subscribers)} подписчиков для пользователя {data['author_id']}")
            for sub in subscribers:
                user = await UserRepository(db).filter_by_spec(
                    UserSpecification.id_is(sub.subscriber_user_id)
                )
                if user:
                    if user[0].subscription_key:
                        await send_push(token=user[0].subscription_key, message=message)
                    else:
                        logger.warning(f"У подписчика {sub.subscriber_user_id} нет subscription_key")
                else:
                    logger.warning(f"Подписчик {sub.subscriber_user_id} не найден в базе")

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

# ------------------ Worker ------------------
async def worker():
    while True:  # бесконечный цикл на reconnect
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
