from kafka import KafkaConsumer
import json
from kafka import KafkaProducer
from compile import compile_code

# Consumes messages sent to the 'code' topic
listener_consumer = KafkaConsumer(
    'code',
    bootstrap_servers = ['localhost:9092'],
    api_version = (0, 10, 1))

# Compiles the code and sends the result to the 'result' topic
response_producer =  KafkaProducer(
    bootstrap_servers = ['localhost:9092'],
    api_version=(0, 10, 1),
    value_serializer=lambda v: json.dumps(v).encode('utf-8'))

# Read data from kafka
def compile_from_listener_and_send_to_response_queue():
    for message in listener_consumer:
        message = message.value.decode('utf-8')    # Decode the message
        result = compile_code(json.loads(message)) # Compile the code
        future = response_producer.send('result', result)   # Send the result to the result topic
        res = future.get(timeout=60)
        print("output sent to response queue\n {}".format(res))
        response_producer.flush()
    
def main():
    while True:
        compile_from_listener_and_send_to_response_queue() # run forever

main()