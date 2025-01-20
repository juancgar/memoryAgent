package main

import (
	"context"
	"fmt"
	"log"
	"os"

	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

func connectMongoDB() *mongo.Client {

	loadEnv()

	client, err := mongo.Connect(context.Background(), options.Client().ApplyURI(os.Getenv("MONGO_URI")))
	if err != nil {
		log.Fatalf("Failed to connect to MongoDB: %v", err)
	}

	err = client.Ping(context.Background(), nil)
	if err != nil {
		log.Fatalf("Failed to ping MongoDB: %v", err)
	}

	fmt.Println("Connected to MongoDB successfully")
	return client
}

func insertIntoMongoDB(client *mongo.Client, collectionName string, data map[string]interface{}) error {
	collection := client.Database("Memories").Collection(collectionName)

	// Convert the data map to BSON format
	document := bson.M(data)

	// Insert the document into the collection
	_, err := collection.InsertOne(context.Background(), document)
	if err != nil {
		return fmt.Errorf("failed to insert document: %v", err)
	}

	return nil
}

func queryMongoDB(client *mongo.Client,
	collectionName string,
	query map[string]interface{}) ([]bson.M, error) {

	collection := client.Database("Memories").Collection(collectionName)
	filter := bson.M(query["filter"].(map[string]interface{}))
	opts := options.Find()
	if limit, ok := query["limit"].(int32); ok {
		opts.SetLimit(int64(limit))
	}

	cursor, err := collection.Find(context.Background(), filter, opts)
	if err != nil {
		return nil, err
	}
	defer cursor.Close(context.Background())

	var results []bson.M
	if err := cursor.All(context.Background(), &results); err != nil {
		return nil, err
	}

	return results, nil
}

func queryWeaviate(client *mongo.Client,
	collectionName string,
	query map[string]interface{}) {
	fmt.Println("Placeholder weaviate")
}
