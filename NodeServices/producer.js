const { Kafka } = require("kafkajs");

class KafkaProducer {
  constructor(broker) {
    this.kafka = new Kafka({ brokers: [broker] });
    this.producer = this.kafka.producer();
  }

  async connect() {
    await this.producer.connect();
    console.log("Kafka producer connected");
  }

  async sendMessage(topic, message) {
    try {
      await this.producer.send({
        topic,
        messages: [{ value: JSON.stringify(message) }],
      });
      console.log(`Message sent to topic ${topic}`);
    } catch (error) {
      console.error("Error sending message to Kafka:", error.message);
      throw error;
    }
  }
}

module.exports = KafkaProducer;