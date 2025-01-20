from confluent_kafka import Producer
import json

def send_insertion_request(data):
    producer = Producer({'bootstrap.servers': 'localhost:9092'})
    topic = 'data_processing_mongo'

    producer.produce(topic, value=json.dumps(data))
    producer.flush()
    print(f"Sent insertion request: {data}")

def send_data_request(request_id, query_params):
    producer = Producer({'bootstrap.servers': 'localhost:9092'})
    topic = 'data_request'

    request = {
        "request_id": request_id,
        "source": "mongo",  # Could be "mongo" or "weaviate"
        "collection": "users",  # Collection (MongoDB) or class (Weaviate)
        "query": query_params  # Query parameters for MongoDB or Weaviate
    }


    producer.produce(topic, value=json.dumps(request))
    producer.flush()
    print(f"Sent data request: {request}")



# Example usage
data_to_insert = {
    "collection": "users",
    "data": {
        "name": "Jenn Test 2",
        "email": "johndoe@exampletest.com",
        "age": 34
    }
}
#send_insertion_request(data_to_insert)
send_data_request("req-123", {"filter": {"age": {"$gte": 25}}, "limit": 10})

