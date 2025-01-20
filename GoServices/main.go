package main

import (
	"context"
	"fmt"
	"os"
	"os/signal"
	"syscall"
)

func main() {
	// Create a context for graceful shutdown
	ctx, cancel := context.WithCancel(context.Background())

	// Handle OS signals
	go func() {
		sigchan := make(chan os.Signal, 1)
		signal.Notify(sigchan, os.Interrupt, syscall.SIGTERM)
		<-sigchan
		fmt.Println("Received shutdown signal, exiting...")
		cancel()
	}()

	groupID := "go-service-group"

	mongoClient := connectMongoDB()
	defer mongoClient.Disconnect(ctx)

	go consumeInsertionRequests(ctx, "data_processing_mongo", groupID, mongoClient)

	go consumeDataRequest(ctx, "data_request", groupID, mongoClient)

	// Wait until the context is canceled
	<-ctx.Done()
	fmt.Println("Service stopped cleanly.")
}
