const { MongoClient } = require("mongodb");

class MongoDBClient {
  constructor(uri) {
    this.client = new MongoClient(uri);
  }

  async connect() {
    try {
      await this.client.connect();
      console.log("Connected to MongoDB");
    } catch (error) {
      console.error("Error connecting to MongoDB:", error.message);
      throw error;
    }
  }

  async queryData(collectionName, filter) {
    try {
      const collection = this.client.db("Memories").collection(collectionName);
      return await collection.find(filter).toArray();
    } catch (error) {
      console.error("Error querying MongoDB:", error.message);
      throw error;
    }
  }

  async insertData(collectionName, data) {
    try {
      const collection = this.client.db("Memories").collection(collectionName);
      const result = await collection.insertOne(data);
      return result.insertedId;
    } catch (error) {
      console.error("Error inserting into MongoDB:", error.message);
      throw error;
    }
  }
}

module.exports = MongoDBClient;
