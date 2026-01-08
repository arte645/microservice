import asyncio
import json
import logging
import aio_pika
from aio_pika.exceptions import ChannelClosed
from aiormq.exceptions import DeliveryError

connection: aio_pika.RobustConnection | None = None
channel: aio_pika.Channel | None = None

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


async def get_channel(queue: str) -> aio_pika.Channel:
    global connection, channel

    if channel and not channel.is_closed:
        return channel

    connection = await aio_pika.connect_robust(
        "amqp://guest:guest@rabbitmq/"
    )

    # 👇 ВАЖНО
    channel = await connection.channel(publisher_confirms=True)

    dlx_name = f"{queue}.dlx"
    dlq_name = f"{queue}.dlq"

    dlx = await channel.declare_exchange(
        dlx_name,
        aio_pika.ExchangeType.DIRECT,
        durable=True
    )

    dlq = await channel.declare_queue(dlq_name, durable=True)
    await dlq.bind(dlx, routing_key=dlq_name)

    try:
        await channel.declare_queue(queue, passive=True)
        return channel
    except aio_pika.exceptions.ChannelClosed:
        channel = await connection.channel(publisher_confirms=True)

    await channel.declare_queue(
        queue,
        durable=True,
        arguments={
            "x-dead-letter-exchange": dlx_name,
            "x-dead-letter-routing-key": dlq_name,
        },
    )

    return channel


MAX_RETRIES = 3
RETRY_DELAY = 1.0


async def publish_notification(message: dict, queue: str):
    channel = await get_channel(queue)

    body = json.dumps(message).encode()

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            await channel.default_exchange.publish(
                aio_pika.Message(
                    body=body,
                    delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
                ),
                routing_key=queue,
                mandatory=True,
            )
            return

        except (
            aio_pika.exceptions.DeliveryError,
            aio_pika.exceptions.AMQPException,
        ) as e:
            if attempt == MAX_RETRIES:
                raise
            await asyncio.sleep(2 ** attempt)
