import asyncio
import os
from dotenv import load_dotenv
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console

# Load environment variables
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in .env file")

# Initialize OpenAI client
model_client = OpenAIChatCompletionClient(model='gpt-4o', api_key=api_key)

# Configure agents with distinct roles
writer = AssistantAgent(
    name='Writer',
    description='A creative poet',
    model_client=model_client,
    system_message='Write a concise 3-line poem (under 30 words) based on the given theme.'
)

reviewer = AssistantAgent(
    name='Reviewer',
    description='A poetry critic',
    model_client=model_client,
    system_message='Review the poem for clarity and imagery in under 30 words. Suggest one improvement.'
)

editor = AssistantAgent(
    name='Editor',
    description='A poetry editor',
    model_client=model_client,
    system_message='Edit the poem based on feedback, keeping it 3 lines and under 30 words.'
)

# Initialize round-robin group chat with max 3 turns
team = RoundRobinGroupChat(
    participants=[writer, reviewer, editor],
    max_turns=3
)

async def run_poem_generator():
    """Run the multi-agent poem generation with feedback loop."""
    task = 'Write a 3-line poem about the sky'
    
    while True:
        try:
            # Run the team chat and stream output
            stream = team.run_stream(task=task)
            await Console(stream)
            print("\nPoem cycle complete!")
            
            # Get user feedback
            feedback = input("Provide feedback (e.g., 'Make it more vivid') or type 'exit' to stop: ")
            if feedback.lower().strip() == 'exit':
                print("Exiting poem generator.")
                break
            
            # Update task with feedback
            task = f"Revise the poem based on this feedback: {feedback}"
        
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            break

if __name__ == "__main__":
    asyncio.run(run_poem_generator())