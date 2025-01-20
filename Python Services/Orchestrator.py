import os
import utilitis as helper

class Orchestrator:

    llm = helper.initilize_chat_gpt(key=os.environ["OPENAI_API_KEY"])
    weaview_client = None
    is_vdb_running = False
    is_llm_running = False

    def initialize_VDB():
        if not is_vdb_running :
            return "Client already running"
        else: 
            weaview_client = helper.initialize_weaview(os.environ["WCD_URL"], 
                                                os.environ["WCD_API_KEY"], 
                                                os.environ["OPENAI_API_KEY"])
            return "Client running"
    def initialize_LLM():
        if not is_llm_running :
            return "Chat GPT already running"
        else: 
            try:
                llm = helper.initilize_chat_gpt(key=os.environ["OPENAI_API_KEY"])
                is_vdb_running = True
            except:
                return f"chat gpt initialization failed with error code{is_vdb_running}"
            return "Chat GPT running"
        

        
    def create_collection(name,description=None):
        weaview_client.collections.create(
        name="episodic_memory",
        description="Collection containing historical chat interactions and takeaways.",
        vectorizer_config=Configure.Vectorizer.text2vec_openai(), # Change to text2vec-openai for Weaviate Cloud
        properties=[
            Property(name="conversation", data_type=DataType.TEXT),
            Property(name="context_tags", data_type=DataType.TEXT_ARRAY),
            Property(name="conversation_summary", data_type=DataType.TEXT),
            Property(name="what_worked", data_type=DataType.TEXT),
            Property(name="what_to_avoid", data_type=DataType.TEXT),
            Property(name="emotion_tags", data_type=DataType.TEXT_ARRAY)

        ]
    )


