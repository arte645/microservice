import json
import aio_pika
from aio_pika.exceptions import ChannelClosed

connection: aio_pika.RobustConnection | None = None
channel: aio_pika.Channel | None = None


async def get_channel(queue: str) -> aio_pika.Channel:
    global connection, channel

    if channel and not channel.is_closed:
        return channel

    connection = await aio_pika.connect_robust(
        "amqp://guest:guest@rabbitmq/"
    )
    channel = await connection.channel()

    dlx_name = f"{queue}.dlx"
    dlq_name = f"{queue}.dlq"

    dlx = await channel.declare_exchange(
        dlx_name,
        aio_pika.ExchangeType.DIRECT,
        durable=True
    )

    dlq = await channel.declare_queue(
        dlq_name,
        durable=True
    )

    await dlq.bind(dlx, routing_key=dlq_name)

    try:
        await channel.declare_queue(queue, passive=True)
        return channel

    except ChannelClosed:
        channel = await connection.channel()

    await channel.declare_queue(
        queue,
        durable=True,
        arguments={
            "x-dead-letter-exchange": dlx_name,
            "x-dead-letter-routing-key": dlq_name,
        },
    )

    return channel


async def publish_notification(message: dict, queue: str):
    channel = await get_channel(queue)

    await channel.default_exchange.publish(
        aio_pika.Message(
            body=json.dumps(message).encode(),
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
        ),
        routing_key=queue,
        mandatory=True,
    )
