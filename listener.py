import tornado.web
import tornado.websocket
import tornado.ioloop
from kafka import KafkaProducer, KafkaConsumer
import json

# Consumer for output from compiler
response_consumer = KafkaConsumer(
    'result',
    bootstrap_servers = ['localhost:9092'],
    api_version=(0, 10, 1),
    value_deserializer=lambda m: json.loads(m.decode('utf-8')))

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print("New client connected")
        for response in response_consumer:
            print(response.value)
            self.write_message(response.value)

    def on_close(self):
        print("Client disconnected")

    def check_origin(self, origin):
        return True

application = tornado.web.Application([
        (r"/", WebSocketHandler),
])

if __name__ == "__main__":
    application.listen(8766)
    loop = tornado.ioloop.IOLoop.instance()
    #loop.add_callback(fun())
    loop.start()