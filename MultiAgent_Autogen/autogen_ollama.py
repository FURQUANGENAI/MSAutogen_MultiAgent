from autogen_core.models import UserMessage
from autogen_ext.models.ollama import OllamaChatCompletionClient
import asyncio

# Initialize the Ollama client
ollama_model_client = OllamaChatCompletionClient(model="llama3.2")

# Define the async function
async def main():
    response = await ollama_model_client.create([UserMessage(content="Why should I take Supplements for Body building"
                                                             "Is it Necessary? simple answer and benefits would be helpful", source="user")])
    with open("output.txt", "w") as f:
        f.write(response.content)
    print("Response saved to output.txt")
    await ollama_model_client.close()

# Run the async function
if __name__ == "__main__":
    asyncio.run(main())