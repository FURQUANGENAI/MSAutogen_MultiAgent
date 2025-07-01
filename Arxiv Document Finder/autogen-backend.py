import streamlit as st
import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_ext.models.openai import OpenAIChatCompletionClient
import os
import arxiv
from typing import List, Dict
from datetime import datetime

# Initialize OpenAI client
openai_brain = OpenAIChatCompletionClient(
    model='gpt-4o',
    api_key=os.getenv('OPENAI_API_KEY')
)

def arxiv_search(query: str, max_results: int = 5) -> List[Dict]:
    """Return a list of arXiv papers matching the query."""
    try:
        client = arxiv.Client()
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.Relevance,
        )
        papers = []
        for result in client.results(search):
            papers.append({
                "title": result.title,
                "authors": [a.name for a in result.authors],
                "published": result.published.strftime("%Y-%m-%d"),
                "summary": result.summary,
                "pdf_url": result.pdf_url,
            })
        return papers
    except Exception as e:
        return [{"error": f"arXiv search failed: {str(e)}"}]

# Configure agents
arxiv_researcher_agent = AssistantAgent(
    name='arxiv_search_agent',
    description='Creates arXiv queries and retrieves candidate papers',
    model_client=openai_brain,
    tools=[arxiv_search],
    system_message=(
        "Given a user topic, craft an optimal arXiv query. When the tool "
        "returns results, select exactly the number of papers requested and "
        "pass them as concise JSON to the summarizer."
    ),
)

summarizer_agent = AssistantAgent(
    name='summarizer_agent',
    description='Summarizes research papers',
    model_client=openai_brain,
    system_message=(
        "You are an expert researcher. When you receive a JSON list of papers, "
        "write a literature review in Markdown:\n"
        "1. Start with a 2–3 sentence introduction of the topic.\n"
        "2. Include one bullet per paper with: title (as Markdown link), "
        "authors, specific problem tackled, and key contribution.\n"
        "3. End with a single-sentence takeaway."
    ),
)

# Set up team
team = RoundRobinGroupChat(
    participants=[arxiv_researcher_agent, summarizer_agent],
    max_turns=2
)

# Streamlit app
st.title("arXiv Literature Review Generator")
st.write("Enter a research topic to generate a literature review based on arXiv papers.")

# User input
topic = st.text_input("Research Topic", value="Autogen")
num_papers = st.slider("Number of Papers", min_value=1, max_value=10, value=5)
search_button = st.button("Generate Literature Review")

# Placeholder for results
result_container = st.container()

async def run_search(topic: str, num_papers: int) -> str:
    task = f"Conduct a literature review on the topic '{topic}' and return exactly {num_papers} papers."
    result = ""
    async for msg in team.run_stream(task=task):
        result += f"{msg}\n"
    return result

def main():
    if search_button:
        if not topic.strip():
            st.error("Please enter a valid research topic.")
            return
        if not os.getenv('OPENAI_API_KEY'):
            st.error("OPENAI_API_KEY environment variable not set.")
            return
        
        with result_container:
            with st.spinner("Generating literature review..."):
                try:
                    # Run the async task in Streamlit
                    result = asyncio.run(run_search(topic, num_papers))
                    st.markdown(result)
                except Exception as e:
                    st.error(f"Error generating review: {str(e)}")

if __name__ == "__main__":
    main()