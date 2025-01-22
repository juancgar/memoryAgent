const weaviate = require("weaviate-client");

class WeaviateClient {
  constructor(baseURL, apiKey, openAIKey) {
    this.client = null
    this.apiKey = apiKey
    this.baseURL = baseURL
    this.openAIKey = openAIKey
  }

  async connect(){
    try{
    console.log("Initializing Weaviate client...");
    this.client = await weaviate.connectToWeaviateCloud(this.baseURL,{
      authCredentials: new weaviate.ApiKey(this.apiKey),
      headers: {
        'X-OpenAI-Api-Key': this.openAIKey|| '',  // Replace with your inference API key
      }
    });
    console.log("Connected to Weaviate client");
  }
  catch(error)
  {
    console.error("Error connecting to Weaviate Cloud:", error.message);
    throw error
  }


  }

  // Perform a hybrid query
  async hybridQuery(className, searchQuery, alpha, limit) {
    try {
      if (!this.client) {
        throw new Error("Weaviate client is not initialized. Call `connect()` first.");
      }
      const collection = this.client.collections.get(className)
      result = await collection.query.hybrid(searchQuery, {
        limit: limit , alpha:alpha
      })
        
      console.log("Weaviate Hybrid Query Result:", JSON.stringify(result, null, 2));
      return result;
    } catch (error) {
      console.error("Error performing hybrid query:", error.message);
      throw error;
    }
  }

  // Insert data into Weaviate
  async insertData(className, data) {
    try {
      const result = await this.client.data
        .creator()
        .withClassName(className)
        .withProperties(data)
        .do();

      console.log("Data Inserted Successfully:", JSON.stringify(result, null, 2));
      return result;
    } catch (error) {
      console.error("Error inserting data into Weaviate:", error.message);
      throw error;
    }
  }
}

module.exports = WeaviateClient;
