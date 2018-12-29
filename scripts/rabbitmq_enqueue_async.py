#! which(python3.6)

import json

import asyncio
import aio_pika


async def main(loop):
    connection = await aio_pika.connect_robust(
        'amqp://guest:guest@127.0.0.1/',
        loop=loop
    )

    async with connection:
        routing_key = 'envelops_queue'
        message = {'target_id': 1, 'message': 'sample message'}

        channel = await connection.channel()

        await channel.default_exchange.publish(
            aio_pika.Message(
                body=bytes(json.dumps(message), 'utf-8')
            ),
            routing_key=routing_key
        )


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
    loop.close()

