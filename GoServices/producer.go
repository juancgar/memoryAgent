package main

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"os"
	"time"

	"github.com/joho/godotenv"
	"github.com/segmentio/kafka-go"
)

func loadEnv() {
	// Load the .env file
	err := godotenv.Load()
	if err != nil {
		log.Fatalf("Error loading .env file: %v", err)
	}
}

func produceMessage(topic, message string) {
	// Load environment variables
	loadEnv()

	// Get Kafka broker address from the environment
	brokerAddress := os.Getenv("KAFKA_BROKER")
	if brokerAddress == "" {
		log.Fatal("KAFKA_BROKER is not set in the environment")
	}

	writer := kafka.NewWriter(kafka.WriterConfig{
		Brokers:  []string{brokerAddress},
		Topic:    topic,
		Balancer: &kafka.LeastBytes{},
	})

	defer writer.Close()

	err := writer.WriteMessages(context.Background(),
		kafka.Message{
			Key:   []byte(fmt.Sprintf("Key-%d", time.Now().Unix())),
			Value: []byte(message),
		},
	)
	if err != nil {
		log.Fatalf("Failed to write message: %v", err)
	}

	fmt.Printf("Message '%s' sent to topic '%s'\\n", message, topic)
}

func publishDataResponse(topic, requestID string, result interface{}) {
	loadEnv()
	brokerAddress := os.Getenv("KAFKA_BROKER")
	if brokerAddress == "" {
		log.Fatal("KAFKA_BROKER is not set in the environment")
	}
	writer := kafka.NewWriter(kafka.WriterConfig{
		Brokers:  []string{brokerAddress},
		Topic:    topic,
		Balancer: &kafka.LeastBytes{},
	})

	defer writer.Close()

	response := map[string]interface{}{
		"request_id": requestID,
		"data":       result,
	}

	jsonResponse, err := json.Marshal(response)
	if err != nil {
		log.Printf("Parsing data request response failed %v\n", err)
		return
	}

	err = writer.WriteMessages(context.Background(),
		kafka.Message{
			Key:   []byte(requestID),
			Value: jsonResponse,
		},
	)
	if err != nil {
		log.Fatalf("Failed to publish response: %v", err)
	} else {
		fmt.Printf("Response for request '%s' published successfully\n", requestID)
	}

}
