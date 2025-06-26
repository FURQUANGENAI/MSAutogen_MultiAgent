AutoGen Multi-Tool Agent
This project demonstrates how to use AutoGen 0.6.1 to create an AI agent capable of performing various tasks using custom tools. The agent leverages the FunctionTool class from autogen_core.tools to register and use multiple tools, including text reversal, text summarization, file reading, arithmetic calculations, and webpage fetching.
Features

Text Reversal: Reverses the characters in a given text string.
Text Summarization: Truncates text to a specified length to create concise summaries.
File Reading: Reads the contents of text files (.txt or .md).
Arithmetic Calculations: Evaluates basic arithmetic expressions.
Webpage Fetching: Fetches webpage content and converts it to markdown format.
OpenAI Integration: Uses the gpt-4o-mini model via OpenAIChatCompletionClient for intelligent task handling.
Asynchronous Execution: Supports async tools for efficient webpage fetching.

Prerequisites

Python 3.8 or higher
An OpenAI API key (set in a .env file as OPENAI_API_KEY)

Installation

Clone this repository or download the code.

Install the required dependencies:
pip install autogen-agentchat autogen-ext openai python-dotenv httpx beautifulsoup4 html2text


Create a .env file in the project root with your OpenAI API key:
OPENAI_API_KEY=your-api-key-here



Usage

Save the main script as multi_tool_agent.py (or use the provided script).

Run the script:
python multi_tool_agent.py


The default task in the script is to calculate the result of 5 + 3 * 2 and reverse the result. Modify the task variable in the script to try different tasks.


Example Tasks

Reverse Text: "Reverse the text 'Welcome to AI!'"
Output: "!IA ot emocleW"


Summarize Text: "Summarize this text to 30 characters: 'The quick brown fox jumps over the lazy dog.'"
Output: "The quick brown fox jumps..."


Read File: "Read the contents of 'config.txt'."
Output: Contents of config.txt (file must exist).


Calculate: "Calculate the result of '10 / 2 + 3'."
Output: "8.0"


Fetch Webpage: "Fetch the content of 'https://example.com' and summarize it to 200 characters."
Output: Markdown content of the webpage, truncated to 200 characters.



Example Code
The main script (multi_tool_agent.py) initializes an AssistantAgent with five tools and runs a task. Below is a snippet of the key components:
# Initialize the OpenAI model client
openai_client = OpenAIChatCompletionClient(model="gpt-4o-mini", api_key=api_key)

# Register tools
reverse_tool = FunctionTool(reverse_string, description="Reverses the order of characters in a given text string.")
summarize_tool = FunctionTool(summarize_text, description="Summarizes a given text to a specified length.")
file_read_tool = FunctionTool(read_text_file, description="Reads the contents of a text file (.txt or .md).")
calc_tool = FunctionTool(calculate_expression, description="Evaluates a basic arithmetic expression.")
fetch_webpage_tool = FunctionTool(fetch_webpage, description="Fetches a webpage and converts its content to markdown.")

# Create agent
agent = AssistantAgent(
    name="MultiToolAgent",
    model_client=openai_client,
    system_message="You are a helpful assistant that can reverse text, summarize text, read files, perform calculations, and fetch webpages using the provided tools.",
    tools=[reverse_tool, summarize_tool, file_read_tool, calc_tool, fetch_webpage_tool],
    reflect_on_tool_use=True,
)

# Run a task
task = "Calculate the result of '5 + 3 * 2' and then reverse the result."
result = await agent.run(task=task)
print(f"Agent Response: {result.messages[-1].content}")

Tools Overview

reverse_string: Reverses the characters in a string.
Example: "Hello" → "olleH"


summarize_text: Truncates text to a specified length.
Example: "Long text here", max_length=10 → "Long text..."


read_text_file: Reads contents of .txt or .md files.
Example: Reads notes.txt and returns its content.


calculate_expression: Evaluates arithmetic expressions.
Example: "2 + 3 * 4" → 14.0


fetch_webpage: Fetches a webpage and converts it to markdown.
Example: Fetches https://example.com and returns markdown content.



Notes

Ensure the .env file contains a valid OPENAI_API_KEY.
The fetch_webpage tool requires internet access and may raise errors for invalid URLs or unreachable pages.
The read_text_file tool requires the specified file to exist in the project directory.
The calculate_expression tool supports basic arithmetic (+, -, *, /) and uses eval with restricted inputs for safety.
Modify the system_message and tool descriptions to improve the agent's tool selection accuracy.

Troubleshooting

API Key Error: Ensure OPENAI_API_KEY is set in the .env file.
Module Not Found: Install all dependencies listed in the Installation section.
File Not Found: Ensure the file exists for read_text_file tasks.
Network Errors: Check internet connectivity for fetch_webpage tasks.

Contributing
Feel free to submit issues or pull requests to enhance the tools or add new ones. Suggestions for improving tool descriptions, error handling, or additional use cases are welcome.
License
This project is licensed under the MIT License Developed by Furquan using Autogen 0.6.1(stable)