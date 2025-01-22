from coreAi import coreAi
import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage



dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')

# Load the .env file
load_dotenv(dotenv_path)
jenne_ai = coreAi([],set(),set(),os.getenv('OPEN_API_KEY'))

jenne_ai.start()
