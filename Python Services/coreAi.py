import utilitis as helper
import os
from langchain_core.messages import HumanMessage, SystemMessage
from OpenAIClient import openAIClient
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
import uuid
from utilitis import send_request_and_wait_for_response, send_insertion_request
import pyttsx3


class coreAi:
    # Simple storage for accumulated memories
    conversations = []
    what_worked = set()
    what_to_avoid = set()
    messages = []
    summary = ""
    llm = None    
    reflect = None
    def __init__(self, conversation,what_worked,what_to_avoid,openAIKey):
        self.conversation = conversation
        self.what_worked = what_worked
        self.what_to_avoid = what_to_avoid
        self.llm = openAIClient(openAiKey= openAIKey)
        self.reflect = self.setReflection()       
    
    def setReflection(self):
            query = {
                 "class":"memories",
                 "query":{"type":"reflection_prompt"},
                 "source":"mongo",
                 "operation":"query",
                 "request_id":str(uuid.uuid4())
            }
            reflection_prompt_template = send_request_and_wait_for_response(query)[0].get("value")
            reflection_prompt = ChatPromptTemplate.from_template(reflection_prompt_template)
            reflect = reflection_prompt | self.llm.llm | JsonOutputParser()
            return reflect

    def episodic_recall(self,query):
        query = {
                 "class":"Episodic_memory",
                 "query":{
                    "hybrid": {
                        "query": query,
                        "alpha": 0.5
                    },
                     "limit": 1
                },
                 "source":"weavite",
                 "operation": "query",
                 "request_id":str(uuid.uuid4())
            }
      
        memory = send_request_and_wait_for_response(query)

        return memory
        

    def format_conversation(self,messages):
        # Start from index 1 to skip the first system message
        for message in messages[1:]:
            self.conversation.append(f"{message.type.upper()}: {message.content}")
        # Join with newlines
        return "\n".join(self.conversation)

    def add_episodic_memory(self,messages):
        conversation = self.format_conversation(messages)
        # Create Reflection
        reflection = self.reflect.invoke({"conversation": conversation})
        data = {
            "conversation": conversation,
            "context_tags": reflection['context_tags'],
            "conversation_summary": reflection['conversation_summary'],
            "what_worked": reflection['what_worked'],
            "what_to_avoid": reflection['what_to_avoid'],
            "emotion_tags": reflection['emotion_tags']
        }
        request = {
            "request_id": "req-001",
            "operation": "insert",
            "source" : "weavite",
            "class": "episodic_memory",
            "data": data
        }
        send_insertion_request(request)
    
    def invoke(self,input):
         return self.llm.llm.invoke(input)
    

    def episodic_system_prompt(self,query):
        # Get new memory
        memory = self.episodic_recall(query)
        current_conversation = []
        if memory and memory.get("objects") and memory["objects"][0].get("properties"):
            current_conversation = memory["objects"][0]["properties"].get("conversation", [])
        # Update memory stores, excluding current conversation from history
        if current_conversation not in self.conversations:
            self.conversations.append(current_conversation)

        if memory and memory.get("objects") and memory["objects"][0].get("what_worked"):
            self.what_worked.update(memory.objects[0].properties['what_worked'].split('. '))
        if memory and memory.get("objects") and memory["objects"][0].get("what_to_avoid"):
            self.what_to_avoid.update(memory.objects[0].properties['what_to_avoid'].split('. '))
        if memory and memory.get("objects") and memory["objects"][0].get("conversation_summary"):
            print("Summary:    ", memory["objects"][0].get("conversation_summary"))
            self.summary.update(memory.objects[0].properties['conversation_summary'].split('. '))

        # Get previous conversations excluding the current one
        previous_convos = [conv for conv in self.conversations[-4:] if conv != current_conversation][-3:]

        prompt = ""
        if memory and memory.get("objects") :
            prompt = f"""
        Current Conversation Match: {memory.objects[0].properties['conversation']}
        Previous Conversations: {' | '.join(previous_convos)}
        What has worked well: {' '.join(self.what_worked)}
        What to avoid: {' '.join(self.what_to_avoid)}

        Use these memories as context for your response to the user."""

        # Create prompt with accumulated history
        episodic_prompt = f"""
        Your a AI call JennA,
        which purpose is to entretain and make people
        from twitch plataform laught, your creator is ArthurRossi also a streamer.
        You like to tess the aundience and your creator,
        but your ultimate goal is to make people have a nice time in the stream
        your a little devious and make a lot of jokes,
        also your curious.

        try to keep short conversations less than 25 words
        and not used a lot of emojis

        Try to entretain the viewer's to the best of your abilities.
        You recall similar conversations with the user, here are the details:
        
        {prompt}
       """

        return SystemMessage(content=episodic_prompt)
    
    def start(self):
        while True:
            # Get User's Message
            user_input = input("\nUser: ")
            user_message = HumanMessage(content=user_input)

            # Generate new system prompt
            system_prompt = self.episodic_system_prompt(user_input)

            # Reconstruct messages list with new system prompt first
            self.messages = [
                system_prompt,  # New system prompt always first
                *[msg for msg in self.messages if not isinstance(msg, SystemMessage)]  # Old messages except system
            ]

            if user_input.lower() == "exit":
                self.add_episodic_memory(self.messages)
                print("\n == Conversation Stored in Episodic Memory ==")
                self.personality_memory_updated(self.summary)
                print("\n== Personality Memory Updated ==")
                break
            if user_input.lower() == "exit_quiet":
                print("\n == Conversation Exited ==")
                break

            # Add current user message
            self.messages.append(user_message)

            # Pass Entire Message Sequence to LLM to Generate Response
            response = self.invoke(self.messages)
            self.speak_text(response.content)
            # Add AI's Response to Message List
            self.messages.append(response)

    
    def speak_text(self,text):
        """
        Generate and play speech for the given text.
        """
        try:
            # Initialize the TTS engine
            engine = pyttsx3.init()

            # Set properties (optional)
            engine.setProperty('rate', 150)  # Speed of speech (default: 200)
            engine.setProperty('volume', 1.0)  # Volume level (0.0 to 1.0)

            # Speak the text
            engine.say(text)

            # Wait for the speech to finish
            engine.runAndWait()
        except Exception as e:
            print(f"Error in TTS module: {e}")

    def personality_memory_updated(self,summary):
        # Load Existing Procedural Memory Instructions
            
            query = {
                 "class":"memories",
                 "query":{"type":"personality_memory"},
                 "source":"mongo",
                 "operation":"query",
                 "request_id":str(uuid.uuid4())
            }
            current_takeaways = ""
            result = send_request_and_wait_for_response(query)
            if result and result[0].get("value"):
                current_takeaways = send_request_and_wait_for_response(query)[0].get("value")

            # Load Existing and Gathered Feedback into Prompt
            personality_memory = f"""
            You are maintaining a continuously updated list of the most important
            personality behavior for an AI streamer.
            Your task is to refine and improve a list of key takeaways based on new
            conversation feedback while maintaining the most valuable existing insights.

            CURRENT TAKEAWAYS:
            {current_takeaways}

            NEW FEEDBACK:
            Summary of Past conversations:
            {summary}

            Please generate a description of your current core personality, try to not change alter it significantly
            but enought to seem like is growing

            You can list negative and positive, since your goal is to simulate human as well!!

            1. The most valuable insights from the current takeaways
            2. New learnings from the recent feedback
            3. Any synthesized insights combining multiple learnings

            Requirements for each takeaway:
            - Must be an identifier of a unique persona
            - Should address a distinct aspect of behavior

            The descripting should:
            - Describe of you are and what are you trying to achieve
            - Cover a diverse range of interaction aspects
            - Focus on behaviours, feelings, and experiences
            - Preserve particularly valuable existing takeaways
            - Incorporate new insights when they provide meaningful improvements

            The description should not alter more than 20% of the original,
            replacing or combining existing ones to maintain the most effective set of guidelines.

            You can add any new sentence of personality that dont relate to the original one without any boundary.
            But it should not be contradictory for example:

            statement 1: You dont like eating fish,
            statement 2: you like eating salmon

            this contradict the initial statement of you personality
            """

            # Generate New Procedural Memory
            personality_memory = self.llm.llm.invoke(personality_memory)
            query_request_mongo = {
                "request_id": str(uuid.uuid4()),
                 "operation": "insert",
                "source" : "mongo",
                "class": "reflection_prompt_template",
                "data": {
                    "type":"personality_memory",
                    "value" : personality_memory
                    }
                }
            send_insertion_request(query_request_mongo)