const { kafka } = require("./client")

async function create_topic(topic, partitions = 2) {
    const admin = kafka.admin();
    console.log("Admin connecting...");
    admin.connect();
    console.log("Admin Connection Success...");
  
    console.log("Creating Topic: " , topic);
    await admin.createTopics({
      topics: [
        {
          topic: topic,
          numPartitions: partitions,
        },
      ],
    });
    console.log("Topic Created Success: " , topic);
    console.log("Disconnecting Admin..");
    await admin.disconnect();
  }
  create_topic("data_responses")
