from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv
import os

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
openai_model_client = OpenAIChatCompletionClient(api_key=openai_api_key, model="gpt-4o-mini")

model_client = OpenAIChatCompletionClient(api_key=openai_api_key, model="gpt-4o-mini")
my_first_agent = AssistantAgent(model_client=model_client, name="my_first_agent")








