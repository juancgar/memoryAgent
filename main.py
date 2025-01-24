from coreAi import coreAi
import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage



dotenv_path = os.path.join(os.path.dirname(__file__), '.env')

# Load the .env file
load_dotenv(dotenv_path)
openAIToken = os.getenv('OPEN_API_KEY')
discordToken = os.getenv('DISCORD_TOKEN')



jenne_ai = coreAi([],set(),set(),openAIToken,discordToken)
jenne_ai.start_with_await(True,discordToken)
#jenne_ai.start(False,True)
#print(discordToken)


