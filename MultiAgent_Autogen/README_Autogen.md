Multi-Agent Poem Generator
This project leverages AutoGen (version 0.6.1) to create a multi-agent system that collaboratively generates, reviews, and edits a 3-line poem about the sky. Three agents (Writer, Reviewer, Editor) work in a round-robin group chat, with a user feedback loop to refine the poem iteratively.
Features

Multi-Agent Collaboration: Uses RoundRobinGroupChat with three specialized agents:
Writer: Creates a 3-line poem (under 30 words) based on the task.
Reviewer: Critiques the poem and suggests an improvement.
Editor: Revises the poem based on feedback.


OpenAI Integration: Powered by GPT-4o via OpenAIChatCompletionClient.
Feedback Loop: Allows users to provide feedback to refine the poem or exit the process.
Async Streaming: Displays output in real-time using AutoGen’s Console UI.
Error Handling: Includes checks for API key and runtime errors.

Prerequisites

Python 3.8+
An OpenAI API key
AutoGen 0.6.1 and dependencies

Installation

Clone this repository:git clone https://github.com/your-username/multi-agent-poem-generator.git
cd multi-agent-poem-generator


Create and activate a virtual environment:python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install dependencies:pip install autogen-agentchat==0.6.1 python-dotenv


Create a .env file in the project root with your OpenAI API key:echo "OPENAI_API_KEY=your-api-key-here" > .env



Usage

Run the script:python multi_agent_poem_generator.py


The agents will generate, review, and edit a 3-line poem about the sky.
Provide feedback (e.g., “Make it more vivid”) or type exit to stop.
The cycle repeats with your feedback as the new task.

Project Structure

multi_agent_poem_generator.py: Main script implementing the multi-agent workflow.
.env: Stores the OpenAI API key (not tracked in git).

Example Output
Writer: Sky of azure, clouds drift free,  
Stars at night, a cosmic sea,  
Dawn’s soft glow, eternity.  

Reviewer: Clear imagery, but lacks vivid color.  
Suggest: Add vibrant sunset hues.  

Editor: Sky of azure, clouds dance free,  
Sunset blazes, crimson sea,  
Stars ignite eternity.  

Provide feedback (e.g., 'Make it more vivid') or type 'exit' to stop: exit
Exiting poem generator.

Technical Details

Framework: AutoGen 0.6.1, using RoundRobinGroupChat with max_turns=3.
Agents: Three AssistantAgents with distinct system messages for writing, reviewing, and editing.
Feedback Loop: User feedback is framed as a new task (e.g., “Revise the poem based on: [feedback]”).
Error Handling: Validates API key and catches runtime errors for robustness.

Contributing
Submit issues or pull requests to enhance the project. Follow PEP 8 style guidelines.
License
Licensed under the MIT License. See the LICENSE file for details.
Acknowledgments

Built with AutoGen 0.6.1
Powered by OpenAI GPT-4o

