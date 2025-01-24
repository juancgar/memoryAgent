from confluent_kafka import Producer, Consumer
import json
import uuid
import time

# Kafka Configuration
BROKER = "localhost:9092"
DATA_REQUESTS_TOPIC = "data_requests"
DATA_RESPONSES_TOPIC = "data_responses"

def read_config():
  # reads the client configuration from client.properties
  # and returns it as a key-value map
  config = {}
  with open("client.properties") as fh:
    for line in fh:
      line = line.strip()
      if len(line) != 0 and line[0] != "#":
        parameter, value = line.strip().split('=', 1)
        config[parameter] = value.strip()
  return config

# Initialize Kafka Producer
producer = Producer(read_config())
config = read_config()
config["group.id"] = "python-group-1"
config["auto.offset.reset"] = "earliest"

# Initialize Kafka Consumer
consumer = Consumer(config)



def send_request_and_wait_for_response(query_data, timeout=30):
    """
    Send a request to Kafka and wait for a response.
    """
    # Build the request message
    request_message = query_data

    search_id = query_data.get('request_id')

    # Send the message to the data_requests topic
    producer.produce(DATA_REQUESTS_TOPIC, value=json.dumps(request_message))
    producer.flush()
    print(f"Request sent to topic '{DATA_REQUESTS_TOPIC}'")

    # Subscribe to the data_responses topic
    consumer.subscribe([DATA_RESPONSES_TOPIC])

    # Wait for a response
    start_time = time.time()
    while time.time() - start_time < timeout:
        msg = consumer.poll(1.0)  # Poll with a timeout of 1 second
        if msg is None:
            # No message received, continue polling
            continue
        if msg.error():
            print(f"Consumer error: {msg.error()}")
            continue
        try:
            # Parse the response message
            response_message = json.loads(msg.value().decode("utf-8"))
            # Check if this is the response for our request_id
            if response_message.get("request_id") == search_id:
                print("Matching response received! for request: ", search_id)
                return response_message.get("result")
        except json.JSONDecodeError as e:
            print(f"Failed to decode message: {e}")

    
def send_insertion_request(data):
    producer = Producer({'bootstrap.servers': 'localhost:9092'})
    topic = 'data_requests'

    producer.produce(topic, value=json.dumps(data))
    producer.flush()
    print(f"Sent insertion request: {data}")
    

