from langchain_openai import ChatOpenAI
import utilitis as helper
import os
from langchain_core.messages import HumanMessage, SystemMessage
import weaviate
from weaviate.classes.init import Auth

def initilize_chat_gpt(model="gpt-4o", key=""):
    return ChatOpenAI(temperature=0.7, model=model, api_key=key)


def initialize_weaview(wcd_url,wcd_api_key,openai_api_key):
    return weaviate.connect_to_weaviate_cloud(
    cluster_url=wcd_url,  # Replace with your Weaviate Cloud URL
    auth_credentials=Auth.api_key(wcd_api_key),  # Replace with your Weaviate Cloud key
    headers={'X-OpenAI-Api-key': openai_api_key}  # Replace with your OpenAI API key
)