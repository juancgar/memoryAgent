import utilitis as helper
import os
from langchain_core.messages import HumanMessage, SystemMessage
import weaviate
from weaviate.classes.init import Auth

class coreAi:
    # Simple storage for accumulated memories
    conversations = []
    what_worked = set()
    what_to_avoid = set()
    
    



    
