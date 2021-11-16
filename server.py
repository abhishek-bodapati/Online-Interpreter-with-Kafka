import tornado.web
import tornado.websocket
from tornado.ioloop import IOLoop
from tornado import gen
from kafka import KafkaProducer, KafkaConsumer
import json
import uuid
import traceback
from kiel import clients as _clients

clients = {}
LISTEN_PORT = 8765
LISTEN_ADDRESS = '127.0.0.1'

# Kafka producer for code (which is to be sent for compilation)
listener_producer = KafkaProducer(
    bootstrap_servers = ['localhost:9092'],
    api_version=(0, 10, 1),
    value_serializer=lambda v: json.dumps(v).encode('utf-8'))

# Consume the output from response queue and send back to client
@gen.coroutine
def consume():
    c = _clients.SingleConsumer(brokers=["localhost:9092"])

    yield c.connect()

    while True:
        msgs = yield c.consume("result")
        for msg in msgs:
            client_id = json.loads(msg)["client_id"]
            output = json.loads(msg)["output"]
            clients[client_id].write_message(output) # Sends the output to specified client_id

class WebSocketHandler(tornado.websocket.WebSocketHandler):

    def __init__(self, application, request, **kwargs):
        super(WebSocketHandler, self).__init__(application, request, **kwargs)
        # Generate a unique client_id
        self.client_id = str(uuid.uuid4())

    def open(self):
        clients[self.client_id] = self
        print('Connection for client {0} opened!!'.format(self.client_id))

    def on_message(self, message):
        message = json.loads(message)
        message["client_id"] = self.client_id
        message = json.dumps(message)
        try:
            future = listener_producer.send('code', message)
            future.get(timeout=10)
            listener_producer.flush()
            print("Code sent to Kafka Listener Producer")
        except:
            traceback.print_exc()

    def on_close(self):
        x = str(self.client_id)
        clients.pop(self.client_id, None)
        print("Client {} disconnected!!".format(x))

    def check_origin(self, origin):
        return True

application = tornado.web.Application([
        (r"/", WebSocketHandler),
])

if __name__ == "__main__":
    # Setup HTTP Server
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(LISTEN_PORT, LISTEN_ADDRESS)
    loop = IOLoop.instance()
    loop.add_callback(consume)
    try:
        loop.start()
    except KeyboardInterrupt:
        loop.stop()



