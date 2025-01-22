from confluent_kafka import Consumer
import json

# Kafka consumer configuration
consumer_config = {
    'bootstrap.servers': 'localhost:9092',  # Kafka broker(s)
    'group.id': 'python-consumer-group',   # Consumer group ID
    'auto.offset.reset': 'earliest',       # Start reading from the earliest messages
}

# Initialize Kafka Consumer
consumer = Consumer(consumer_config)

# Subscribe to the `data_responses` topic
topic = 'data_responses'
consumer.subscribe([topic])

print(f"Subscribed to topic '{topic}'. Listening for messages...")

try:
    while True:
        # Poll for messages
        msg = consumer.poll(1.0)  # Timeout in seconds

        if msg is None:
            # No message received, continue polling
            continue

        if msg.error():
            print(f"Consumer error: {msg.error()}")
            continue

        # Decode and process the message
        try:
            message_value = json.loads(msg.value().decode('utf-8'))
            print(f"Received message: {message_value}")

            # Extract and process fields from the message
            request_id = message_value.get('request_id')
            result = message_value.get('result')

            if result:
                print(f"Response for request_id '{request_id}': {result}")
            else:
                print(f"Error in response for request_id '{request_id}': {message_value.get('error')}")

        except json.JSONDecodeError as e:
            print(f"Failed to decode message: {e}")

except KeyboardInterrupt:
    print("\nConsumer interrupted. Closing...")
finally:
    # Ensure the consumer is closed properly
    consumer.close()
    print("Consumer closed.")
    