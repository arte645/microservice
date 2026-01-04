import json
import aio_pika
import asyncio

connection: aio_pika.RobustConnection | None = None
channel: aio_pika.Channel | None = None

async def get_channel() -> aio_pika.Channel:
    global connection, channel
    if channel and not channel.is_closed:
        return channel
    connection = await aio_pika.connect_robust("amqp://guest:guest@rabbitmq/")
    channel = await connection.channel()
    await channel.declare_queue("notifications", durable=True)
    return channel

async def publish_notification(message: dict):
    channel = await get_channel()
    await channel.default_exchange.publish(
        aio_pika.Message(
            body=json.dumps(message).encode(),
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT
        ),
        routing_key="notifications",
        mandatory=True
    )
