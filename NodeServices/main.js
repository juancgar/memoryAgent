require("dotenv").config({ path: '/Users/juangarza/Documents/Me/PersonalProjects/Agent/memoryAgent/.env'});
const MongoDBClient = require("./mongo");
const WeaviateClient = require("./weaviate");
const KafkaProducer = require("./producer");
const KafkaConsumer = require("./consumer");


(async () => {
  // Initialize clients


  try {

    const mongoClient = new MongoDBClient(process.env.MONGO_URI);
    const weaviateClient = new WeaviateClient(process.env.WCD_URL, process.env.WCD_API_KEY,process.env.OPEN_API_KEY);
    const producer = new KafkaProducer(process.env.KAFKA_BROKER);
    const consumer = new KafkaConsumer(process.env.KAFKA_BROKER, "node-service-group");
  
    await mongoClient.connect();
    await producer.connect();
    await consumer.connect();
    await weaviateClient.connect();
  
    // Consume messages from Kafka
    await consumer.subscribe("data_requests", async (message) => {
      const { operation, class: className, data, query, request_id } = message;
    // Extract and validate the `hybrid` query
    const { hybrid, limit } = query;
    if (!hybrid || !hybrid.query || typeof hybrid.alpha !== "number") {
      throw new Error("Invalid 'hybrid' query structure");
    }
      try {
        let result;
        if (operation === "query") {
          result = await weaviateClient.hybridQuery(className, hybrid.query , hybrid.alpha, limit);
        } else if (operation === "insert") {
          result = await weaviateClient.insertData(className, data);
        }
        // Send response back to Kafka
        await producer.sendMessage("data_responses", { request_id, result });
      } catch (error) {
        console.error("Error processing message:", error.message);
        await producer.sendMessage("data_responses", { request_id, error: error.message });
      }
    });
    console.log("Consumers are running...");

    // Handle process termination signals for graceful shutdown
    const shutdown = async () => {
      console.log("\nShutting down...");
      await Promise.all([
        consumer.consumer.disconnect(),
        producer.producer.disconnect(),
        mongoClient.client.close(),
      ]);
      console.log("All clients disconnected. Exiting...");
      process.exit(0);
    };

    // Catch termination signals
    process.on("SIGINT", shutdown);
    process.on("SIGTERM", shutdown);
  }
  catch(error) {
    console.error("Error initializing services:", error.message);
    process.exit(1);
  }

})();
