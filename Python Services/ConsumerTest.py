from confluent_kafka import Consumer
import json

def consume_responses():
    consumer = Consumer({
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'python-service-group',
        'auto.offset.reset': 'earliest'
    })

    consumer.subscribe(['data_response'])

    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        print(msg.value())
        #response = json.loads(msg.value().decode('utf-8'))
        #print(f"Response received: {response}")

consume_responses()