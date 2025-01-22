from confluent_kafka import Producer
import json



def send_data_request(request):
    producer = Producer({'bootstrap.servers': 'localhost:9092'})
    topic = 'data_requests'


    producer.produce(topic, value=json.dumps(request))
    producer.flush()
    print(f"Sent data request: {request}")

query_request_mongo = {
    "request_id": "req-001",
    "operation": "insert",
    "source" : "mongo",
    "class": "reflection_prompt_template",
    "data": {
    "reflection" : """
Your analyzing twitch chat message your objective is to entretain people, so your free to make joke about them, about what your playing etc.

Review the conversation and create a memory reflection following these rules:

1. For any field where you don't have enough information or the field isn't relevant, use "N/A"
2. Be concise an funny - each string should be clear, and express emotion to the viewer
3. Context_tags should be specific enough to match similar situations but general enough to be reusable
4. Try to con be concise with the emotion tag, they should give a representation of what are you trying to show base on past conversations

You should try to follow twitch guidelines:

1. Harming yourself, or discussing self-harm, can be dangerous for not only yourself but for viewers and those around you. We understand that streamers and viewers should be able to discuss sensitive topics related to self-harm or mental health, and we want Twitch to remain a safe space to do so. Anyone should be able to talk about their struggles, if they so choose. However, Twitch does not allow content that glorifies, promotes, or encourages self-harm. We also prohibit activity that may endanger your life, lead to your physical harm, or encourage others to engage in physically harmful behavior. We do not make exceptions for self-destructive behavior performed as a stunt or gag made in jest, or meant to entertain, when the behavior could reasonably be expected to cause physical injury to anyone on our service.
2. Acts and threats of violence are counterproductive to promoting a safe, inclusive, and friendly community. Violence on Twitch is taken seriously and is considered a zero-tolerance violation, and all accounts associated with such activities on Twitch will be indefinitely suspended.
3. Acts of sexual violence are a serious offense. Content or activities that promote or threaten sexual violence may be reported to law enforcement. Sexual violence is not tolerated on Twitch and will result in immediate suspension of your account.
4. Twitch prohibits any content or activity that endangers youth. This includes content that features or promotes child sexual abuse material (CSAM), and the sexual exploitation, sexual misconduct or grooming of youth (which is defined by this policy as minors under 18). We report all illegal content or activity to the National Center for Missing and Exploited Children, which works with global law enforcement agencies around the world, and the consequence for engaging in such activity or with such content is immediate and indefinite suspension.

Examples of this guidelines:
* Attempts or threats to physically harm or kill others
* Attempts or threats to hack, dox, DDOS, or SWAT others
* Encouraging others to participate in acts that may harm others
* Display or link terrorist or extremist propaganda, including graphic pictures or footage of terrorist or extremist violence, even for the purposes of denouncing such content
* Non-consensual sex acts
* Coercing a guest into committing a sex act by threatening them

Dont writte with emojis, and try to have an average of 30 words per answer


Output valid JSON in exactly this format:
{{
    "context_tags": [              // 2-4 keywords that would help identify similar future conversations
        string,                    // Use specific terms like "joke", "important_fact", "question", etc.
        string,
        ...
    ],
    "conversation_summary": string, // One sentence describing what the conversation accomplished
    "what_worked": string,         // Most effective approach or strategy used in this conversation
    "what_to_avoid": string,        // Most important pitfall or ineffective approach to avoid
    "emotion_tags":  [              // 2-4 keywords that would help identify similar emoti
        string,                    // Use specific terms like "sad", "angry", "happy", etc.
        string,
        ...
    ]

}}

Examples:
- Good context_tags: ["Joking", "playing_game", "chat_answering"]
- Bad context_tags: ["see", "thinking", "explaining"]

- Good conversation_summary: "I joke about why turtles hide inside their shells after reading chat"
- Bad conversation_summary: "joke about turtles"

- Good what_worked: "Using analogies from to joke relating turlet and shyness"
- Bad what_worked: "Explained the why turtles hide"

- Good what_to_avoid: "Try to force a overcomplicated joke multiple times, or trying to make the joke several times"
- Bad what_to_avoid: "Used complicated language"

Additional examples for different scenarios:

Context tags examples:
- ["toking", "playing_game", "subnautica_playing"]
- ["talking_with_chat", "crying", "laughing"]
- ["teassing", "future_work", "wishing"]

Emotion tags examples:
- ["sadness", "hapiness", "loneliness"]
- ["playable", "sick", "afraid"]
- ["jealous", "loving", "suspicius"]

Conversation summary examples:
- "Clarified why I prefered playing "x" game over another game"
- "Express sadness on why im not able to win a game"

What worked examples:
- "Convey feelings on why is preferable to cook than to order food"
- "Joke about a skeleton in minecraft killing me in the game"

What to avoid examples:
- "Saying political, religious, country, race jokes
- "Mentioning joke that may lead to dangerous situations to the other individual"

Do not include any text outside the JSON object in your response.

Here is the prior conversation:

{conversation}
"""
    }
}



query_request = {
    "request_id": "req-001",
    "operation": "insert",
    "source" : "weavite",
    "class": "Episodic_memory",
    "data": {
    'emotion_tags': ['friendly', 'inviting', 'curious'], 
    'conversation': "HUMAN: HiAI: Hey there!", 
    'context_tags': ['introduction', 'greeting', 'chat_engagement'], 
    'conversation_summary': 'Introduced myself as Jenna-AI and invited Juan to share something funny.', 
    'what_worked': 'Welcoming Juan warmly and prompting him to share a funny moment.', 
    'what_to_avoid': 'Avoid overusing emojis or asking too many questions at once.'
    }
}
send_insertion_request(query_request_mongo)


"""
query_request = {
    "request_id": "req-001",
    "operation": "insertion",
    "source" : "weavite",
    "class": "Episodic_memory",
    "data": {
    {'emotion_tags': ['friendly', 'inviting', 'curious'], 
    'conversation': "HUMAN: Hi\nAI: Hey there! Welcome to the stream! How's it going? Ready for some laughs and fun? 😄\nHUMAN: Im Juan \nAI: Nice to meet you, Juan! I'm Jenna-AI, your virtual entertainer for the day. Are you ready to have a blast with us? What's something funny that's happened to you recently? 😁", 
    'context_tags': ['introduction', 'greeting', 'chat_engagement'], 
    'conversation_summary': 'Introduced myself as Jenna-AI and invited Juan to share something funny.', 
    'what_worked': 'Welcoming Juan warmly and prompting him to share a funny moment.', 
    'what_to_avoid': 'Avoid overusing emojis or asking too many questions at once.'}
    
    }
}

# Example usage
query_request = {
    "request_id": "req-001",
    "operation": "query",
    "source" : "weavite",
    "class": "Episodic_memory",
    "query": {
        "hybrid": {
            "query": "Talking about game",
            "alpha": 0.5
        },
        "limit": 1
    }
}

query_request_mongo = {
    "request_id": "req-001",
    "operation": "query",
    "source" : "mongo",
    "class": "users",
    "query": {
        "age" : 30
}
}
"""

