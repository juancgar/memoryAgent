from langchain_openai import ChatOpenAI



class openAIClient:
    llm = None
    def __init__(self,openAiKey, model = "gpt-4o",temperature = 0.7):
        self.llm = ChatOpenAI(temperature=temperature, model=model, api_key=openAiKey)
        print("Chat GPT model Initization")


