import asyncio
import os
from dotenv import load_dotenv
from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.ui import Console

# Load environment variables
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in .env file")

# Initialize OpenAI client
model_client = OpenAIChatCompletionClient(model='gpt-4o', api_key=api_key)

# Configure Assistant Agent
assistant = AssistantAgent(
    name='PoetAssistant',
    description='A creative assistant that writes poems',
    model_client=model_client,
    system_message='You are a poetic assistant. Write concise, beautiful poems as requested.'
)

# Configure User Proxy Agent (Human in the loop is Furquan)
user_agent = UserProxyAgent(
    name='User',
    description='Represents the user interacting with the assistant',
    input_func=lambda prompt: input(prompt + "\nYour input (type 'APPROVE' to end): ")
)

# Set termination condition
termination_condition = TextMentionTermination('APPROVE')

# Initialize round-robin group chat
team = RoundRobinGroupChat(
    participants=[assistant, user_agent],
    termination_condition=termination_condition
)

# Define the task
task = 'Write a nice 10 -line poem about INDIA'

async def run_poem_generator():
    """Run the poem generation task with error handling."""
    try:
        # Start the team chat and stream output
        stream = team.run_stream(task=task)
        # Display output using Console UI
        await Console(stream)
        print("\nPoem generation complete!")
    except Exception as e:
        print(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    asyncio.run(run_poem_generator())