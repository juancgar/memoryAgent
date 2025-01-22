const { Kafka } = require("kafkajs");

class KafkaConsumer {
    constructor(broker, groupId) {
      this.kafka = new Kafka({ brokers: [broker] });
      this.consumer = this.kafka.consumer({ groupId });
    }

    async connect() {
        await this.consumer.connect();
        console.log("Kafka consumer connected");
  
    }

    async subscribe(topic,onMessage){
        await this.consumer.subscribe({topic,fromBeginning:true})
        await this.consumer.run({
            eachMessage: async ({ topic, partition, message }) => {
              const value = JSON.parse(message.value.toString());
              console.log(`Received message from topic ${topic}:`, value);
              await onMessage(value)
            },
          });
    }
}
module.exports = KafkaConsumer;
