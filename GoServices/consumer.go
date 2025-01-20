package main

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"os"

	"github.com/segmentio/kafka-go"
	"go.mongodb.org/mongo-driver/mongo"
)

func consumeMessages(ctx context.Context, topic, groupID string) {
	// Load environment variables
	loadEnv()

	// Get Kafka broker address from the environment
	brokerAddress := os.Getenv("KAFKA_BROKER")
	if brokerAddress == "" {
		log.Fatal("KAFKA_BROKER is not set in the environment")
	}

	reader := kafka.NewReader(kafka.ReaderConfig{
		Brokers:  []string{brokerAddress},
		Topic:    topic,
		GroupID:  groupID,
		MinBytes: 10e3, // 10KB
		MaxBytes: 10e6, // 10MB
	})

	defer reader.Close()

	fmt.Printf("Listening for messages on topic '%s'...\\n", topic)

	for {
		select {
		case <-ctx.Done():
			fmt.Println("Shutting down consumer...")
			return
		default:
			msg, err := reader.ReadMessage(ctx)
			if err != nil {
				log.Fatalf("Failed to read message: %v", err)
			}
			fmt.Printf("Message received: %s | Key: %s\\n", string(msg.Value), string(msg.Key))
		}
	}
}

// DataInsertionRequest represents the structure of the request
type DataInsertionRequest struct {
	Collection string                 `json:"collection"`
	Data       map[string]interface{} `json:"data"`
}

func consumeInsertionRequests(ctx context.Context, topic, groupID string, mongoClient *mongo.Client) {
	loadEnv()

	reader := kafka.NewReader(kafka.ReaderConfig{
		Brokers:  []string{os.Getenv("KAFKA_BROKER")},
		Topic:    topic,
		GroupID:  groupID,
		MinBytes: 10e3,
		MaxBytes: 10e6,
	})

	defer reader.Close()

	fmt.Printf("Listening for insertion requests on topic '%s'...\n", topic)

	for {
		select {
		case <-ctx.Done():
			fmt.Println("Stopping Kafka consumer...")
			return
		default:
			msg, err := reader.ReadMessage(ctx)
			if err != nil {
				log.Printf("Failed to read message: %v\n", err)
				continue
			}

			fmt.Printf("Message received for insertion: %s\n", string(msg.Value))

			var request DataInsertionRequest
			if err := json.Unmarshal(msg.Value, &request); err != nil {
				log.Printf("Failed to parse message: %v\n", err)
				continue
			}

			// Insert data into MongoDB
			if err := insertIntoMongoDB(mongoClient, request.Collection, request.Data); err != nil {
				log.Printf("Failed to insert data: %v\n", err)
			} else {
				fmt.Printf("Data successfully inserted into collection '%s'\n", request.Collection)
			}
		}
	}
}

// DataRequest represents the structure of the request
type DataRequest struct {
	RequestID  string                 `json:"request_id"`
	Source     string                 `json:"source"`     // "mongo" or"weaviate"
	Collection string                 `json:"collection"` // MongoDB collection or Weaviate class
	Query      map[string]interface{} `json:"query"`      // Query parameters
}

func consumeDataRequest(ctx context.Context,
	topic,
	groupID string,
	mongoClient *mongo.Client) {
	loadEnv()

	reader := kafka.NewReader(kafka.ReaderConfig{
		Brokers:  []string{os.Getenv("KAFKA_BROKER")},
		Topic:    topic,
		GroupID:  groupID,
		MinBytes: 10e3,
		MaxBytes: 10e6,
	})

	defer reader.Close()

	fmt.Printf("Listening for data requests on topic '%s'...\n", topic)

	for {
		select {
		case <-ctx.Done():
			fmt.Println("Stopping Kafka consumer...")
			return
		default:
			msg, err := reader.ReadMessage(ctx)
			if err != nil {
				log.Printf("Failed to read message: %v\n", err)
				continue
			}

			fmt.Printf("Message received for data request: %s\n", string(msg.Value))

			var request DataRequest
			if err := json.Unmarshal(msg.Value, &request); err != nil {
				log.Printf("Failed to parse message: %v\n", err)
				continue
			}

			var result interface{}
			if request.Source == "mongo" {
				result, err = queryMongoDB(mongoClient, request.Collection, request.Query)
			} else if request.Source == "weaviate" {
				result, err = queryMongoDB(mongoClient, request.Collection, request.Query) //queryWeaviate(request.Collection, request.Query)
			}

			if err != nil {
				log.Printf("Failed to query data: %v\n", err)
				continue
			}
			publishDataResponse("data_response", request.RequestID, result)

		}
	}

}
