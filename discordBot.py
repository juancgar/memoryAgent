from discord import Client, Intents, Message
class discordBot:
    def __init__(self):
        print("Initializing discordBot...")
        intents: Intents = Intents.default()
        intents.message_content = True  # Enable message content intent
        self.client = Client(intents=intents)
        if self.client:
            print("Client initialized successfully.")
        else:
            print("Client initialization failed.")

    def start(self, token):
        try:
            self.client.run(token=token)
        except Exception as e:
            print(f"Error while initializing bot: {e}")

    def register_event(self, event_name, handler):
        """
        Register an event handler dynamically.
        """
        if not self.client:
            raise ValueError("Client is not initialized. Ensure `__init__` is called properly.")
        setattr(self.client.event, event_name, handler)

    def on_ready(self, handler):
        """
        Register the on_ready event handler.
        """
        if not self.client:
            raise ValueError("Client is not initialized. Ensure `__init__` is called properly.")

        @self.client.event
        async def on_ready():
            print(f"Bot is ready: {self.client.user}")
            await handler()

    def on_message(self, handler):
        """
        Register the on_message event handler.
        """
        if not self.client:
            raise ValueError("Client is not initialized. Ensure `__init__` is called properly.")

        @self.client.event
        async def on_message(message: Message):
            if message.author == self.client.user:
                return  # Ignore messages from the bot itself
            print(f"Received message: {message.content} from {message.author}")
            await handler(message)
