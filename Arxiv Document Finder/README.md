arXiv Literature Review Generator
Overview
This Streamlit application generates a literature review for a user-specified research topic by querying arXiv papers and summarizing them using AI agents powered by OpenAI's gpt-4o model. It leverages the autogen-agentchat library to coordinate two agents: one for searching arXiv and another for summarizing results into a Markdown-formatted literature review.
Features

User Input: Enter a research topic and select the number of papers (1–10) via a web interface.
arXiv Search: Queries the arXiv API to retrieve relevant papers based on the topic.
AI Agents:
Researcher Agent: Crafts an optimal arXiv query and fetches papers.
Summarizer Agent: Generates a literature review with an introduction, bulleted paper summaries (title as a link, authors, problem, contribution), and a takeaway.


Output: Displays the review in Markdown format.
Error Handling: Validates input and handles API errors.

Requirements

Python 3.8+
Dependencies:pip install streamlit autogen-agentchat autogen-ext arxiv


OpenAI API key (set as an environment variable: OPENAI_API_KEY).

Installation

Clone the repository or save the script as arxiv_search_app.py.
Install dependencies:pip install streamlit autogen-agentchat autogen-ext arxiv


Set the OpenAI API key:export OPENAI_API_KEY='your-api-key'  # On Windows: set OPENAI_API_KEY=your-api-key



Usage

Run the application:streamlit run arxiv_search_app.py


Open the provided URL (e.g., http://localhost:8501) in a browser.
Enter a research topic (e.g., "Autogen"), select the number of papers, and click "Generate Literature Review".
View the generated review in the browser.

Code Structure

OpenAI Client: Uses OpenAIChatCompletionClient with gpt-4o for agent interactions.
arXiv Search: arxiv_search function queries arXiv and returns paper details (title, authors, date, summary, PDF URL).
Agents:
arxiv_researcher_agent: Queries arXiv and passes JSON results to the summarizer.
summarizer_agent: Produces a Markdown literature review.


Team: RoundRobinGroupChat coordinates agents with a maximum of two turns.
Streamlit UI: Includes text input, slider, button, and result display with a loading spinner.
Async Execution: Uses asyncio for agent interactions within Streamlit.

Limitations

Output may include intermediate agent messages (e.g., JSON), reducing readability.
No custom styling for Markdown output (e.g., bullet spacing, link colors).
Async handling may be unstable in some Streamlit environments.

Future Improvements

Filter run_stream output to show only the summarizer’s Markdown.
Add CSS for styled Markdown rendering.
Use Streamlit session state for robust async loop management.
Enhance the summarizer’s system message for stricter Markdown formatting.

Troubleshooting

API Key Error: Ensure OPENAI_API_KEY is set correctly.
Dependency Issues: Update packages: pip install --upgrade streamlit autogen-agentchat autogen-ext arxiv.
Output Formatting: If the review lacks proper bullets, refine the run_search function to filter for Markdown content.

License
MIT License. See LICENSE for details.