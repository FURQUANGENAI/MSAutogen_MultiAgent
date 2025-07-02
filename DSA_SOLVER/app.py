import streamlit as st
import asyncio
from main import get_team_and_docker, run_team
from config.docker_utils import get_docker_executor, start_docker_executor, stop_docker_executor
from config.model_client import get_model_client
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.base import TaskResult

st.set_page_config(page_title="DSA Solver", page_icon="🧑‍💻")
st.title("DSA Solver by Furquan")
st.write("A Streamlit app to solve Data Structures and Algorithms problems using Autogen.")

# Initialize session state for message history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Input for DSA question
task = st.text_input("Enter your DSA Question", value="Can you give me a solution to add 2 numbers?", placeholder="e.g., Find the sum of two numbers")

async def run(team, task, docker):
    try:
        await start_docker_executor(docker)
        async for message in team.run_stream(task=task):
            if isinstance(message, TextMessage):
                yield {"source": message.source, "content": message.content}
            elif isinstance(message, TaskResult):
                yield {"source": "TaskResult", "content": f"Task completed: {message.stop_reason}"}
    except Exception as e:
        yield {"source": "Error", "content": f"An error occurred: {str(e)}"}
    finally:
        await stop_docker_executor(docker)

async def collect_messages(task):
    if not task.strip():
        st.error("Please enter a valid DSA question.")
        return
    team, docker = await get_team_and_docker()
    async for msg in run(team, task, docker):
        st.session_state.messages.append(msg)
        with st.chat_message(msg["source"], avatar={
            "user": "👤",
            "ProblemSolverExpert": "🧑‍💻",
            "CodeExecutorAgent": "🤖",
            "TaskResult": "✅",
            "Error": "❌"
        }.get(msg["source"], "ℹ️")):
            if msg["source"] == "CodeExecutorAgent" and "```" in msg["content"]:
                # Extract code block if present
                code = msg["content"].split("```")[1].strip()
                st.code(code, language="python")
            else:
                st.markdown(msg["content"])

if st.button("Solve"):
    with st.spinner("Solving your question..."):
        try:
            asyncio.run(collect_messages(task))
        except RuntimeError:
            st.error("Asyncio event loop error. Please try again.")