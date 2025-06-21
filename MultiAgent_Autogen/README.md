AutoGen Poem Generator
This project uses AutoGen (version 0.6.1), a Microsoft framework for building agentic AI systems, to create a simple multi-agent application. It features a round-robin group chat between a PoetAssistant (powered by OpenAI's GPT-4o) and a User proxy agent to generate a 4-line poem about India.
Features

Multi-Agent Interaction: Implements a RoundRobinGroupChat with two agents: a poetic assistant and a user proxy.
OpenAI Integration: Uses GPT-4o for creative poem generation.
Async Workflow: Streams output in real-time using AutoGen's Console UI.
Termination Control: Stops the chat when the user types "APPROVE".

Prerequisites

Python 3.8+
An OpenAI API key
AutoGen 0.6.1 and dependencies

Installation

Clone this repository:git clone https://github.com/your-username/autogen-poem-generator.git
cd autogen-poem-generator


Create a virtual environment and activate it:python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install dependencies:pip install autogen-agentchat==0.6.1 python-dotenv


Create a .env file in the project root and add your OpenAI API key:echo "OPENAI_API_KEY=your-api-key-here" > .env



Usage

Run the script:python autogen_poem_generator.py


The PoetAssistant will generate a 4-line poem about India.
Review the poem and type APPROVE to end the session.

Project Structure

autogen_poem_generator.py: Main script implementing the AutoGen workflow.
.env: Environment file for storing the OpenAI API key (not tracked in git).

Example Output
PoetAssistant: In India's heart, where rivers sing,
Colors of culture bloom and spring,
From Himalayan peaks to ocean's shore,
Her timeless spirit forever soars.
User: Type 'APPROVE' to end: APPROVE
Poem generation complete!

Contributing
Feel free to submit issues or pull requests to improve the project. Ensure code follows PEP 8 style guidelines.
License
This project is licensed under the MIT License. See the LICENSE file for details.
Acknowledgments

Built with AutoGen 0.6.1
Powered by OpenAI GPT-4o

