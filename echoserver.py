import tornado.web
import tornado.websocket
import tornado.ioloop
from kafka import KafkaProducer, KafkaConsumer
import json
import time

# Kafka producer for code (which is to be sent to the compiler)
listener_producer = KafkaProducer(
    bootstrap_servers = ['localhost:9092'],
    api_version=(0, 10, 1),
    value_serializer=lambda v: json.dumps(v).encode('utf-8'))

# Consumer for output from compiler
'''response_consumer = KafkaConsumer(
    'result',
    bootstrap_servers = ['localhost:9092'],
    api_version=(0, 10, 1),
    value_deserializer=lambda m: json.loads(m.decode('utf-8')))
'''

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print("New client connected")

    def on_message(self, message):
        future = listener_producer.send('code', message)
        res = future.get(timeout=10)
        listener_producer.flush()
        print(res)

    def on_close(self):
        print("Client disconnected")

    def check_origin(self, origin):
        return True

application = tornado.web.Application([
        (r"/", WebSocketHandler),
])

if __name__ == "__main__":
    application.listen(8765)
    loop = tornado.ioloop.IOLoop.instance()
    #loop.add_callback(fun())
    loop.start()