const {Kafka} = require("kafkajs")

require('dotenv').config({path:'../.env'})

const broker = process.env.KAFKA_BROKER || "localhost:9092"
exports.kafka = new Kafka({
    clientId: "MainCommunicatorClient",
    brokers: [broker],
  });