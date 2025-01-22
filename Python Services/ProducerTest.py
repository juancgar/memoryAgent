from confluent_kafka import Producer
import json

def send_insertion_request(data):
    producer = Producer({'bootstrap.servers': 'localhost:9092'})
    topic = 'data_processing_mongo'

    producer.produce(topic, value=json.dumps(data))
    producer.flush()
    print(f"Sent insertion request: {data}")

def send_data_request(request):
    producer = Producer({'bootstrap.servers': 'localhost:9092'})
    topic = 'data_requests'


    producer.produce(topic, value=json.dumps(request))
    producer.flush()
    print(f"Sent data request: {request}")



# Example usage
query_request = {
    "request_id": "req-001",
    "operation": "query",
    "class": "Episodic_memory",
    "query": {
        "hybrid": {
            "query": "Talking about Python",
            "alpha": 0.5
        },
        "limit": 1
    }
}

# Validate the query
if not query_request["query"]["hybrid"]["query"]:
    raise ValueError("The 'query' field in 'hybrid' is required and cannot be empty.")
if not isinstance(query_request["query"]["hybrid"]["alpha"], (float, int)):
    raise ValueError("The 'alpha' field in 'hybrid' must be a valid float.")

send_data_request(query_request)

