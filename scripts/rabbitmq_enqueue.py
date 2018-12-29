#! which(python3.6)

import json

import pika


MESSAGE = {'field1': 'value1', 'field2': 'value2'}

def enqueue(message: json, queue_name: str):
  message = bytes(json.dumps(message), 'utf-8')
  connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
  channel = connection.channel()
  channel.queue_declare(queue=queue_name)
  channel.basic_publish(exchange='', routing_key=queue_name, body=message)
  print(f' [x] Sent "{message}"')
  connection.close()


if __name__ == '__main__':
  enqueue(MESSAGE, 'test_queue')

