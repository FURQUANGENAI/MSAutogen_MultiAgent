import asyncio
import logging
import os
from autogen_agentchat.agents import CodeExecutorAgent, AssistantAgent
from autogen_ext.code_executors.docker import DockerCommandLineCodeExecutor
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.base import TaskResult
from dotenv import load_dotenv
from docker.errors import DockerException

# Configure logging for better debugging and tracking
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set. Please set it in the .env file or environment.")

# Initialize OpenAI client with GPT-4o-mini model
openai_client = OpenAIChatCompletionClient(model="gpt-4o-mini", api_key=api_key)
logger.info("OpenAI client initialized successfully.")

# Define the ProblemSolverExpert agent for solving the Rat in a Maze problem
problem_solver_expert = AssistantAgent(
    name="ProblemSolverExpert",
    description="An expert agent that solves the Rat in a Maze problem and generates visualizations.",
    model_client=openai_client,
    system_message="""
You are an expert in solving Data Structures and Algorithms (DSA) problems, specializing in the Rat in a Maze problem.
Your tasks are:
1. Provide a clear explanation of how to solve the problem using a backtracking algorithm.
2. Generate Python code in a single block to solve the problem and create a slow-moving GIF (using matplotlib and imageio) to visualize the solution path.
3. Include three diverse test cases: a solvable maze, an unsolvable maze, and an edge-case maze (e.g., 2x2 maze).
4. Print the output of each test case clearly.
5. If the code fails due to missing libraries, provide a shell script with `pip install` commands to install dependencies (e.g., matplotlib, imageio).
6. If an error occurs, provide corrected code in Python block format.
7. Save the GIF as `output.gif` in the working directory.
8. After successful execution, explain the results in detail, including the solution path and test case outcomes.
9. End the conversation with the word "STOP" to terminate the chat.
"""
)

# Define the termination condition for the agent conversation
termination_condition = TextMentionTermination("STOP")
logger.info("Termination condition set to stop on 'STOP' keyword.")

# Initialize Docker-based code executor with a specific Python image
try:
    docker = DockerCommandLineCodeExecutor(
        image="python:3.11-slim",  # Use a lightweight Python image with pre-installed dependencies
        work_dir="tmp",
        timeout=180,  # Increased timeout to accommodate GIF generation
    )
    logger.info("Docker code executor initialized with python:3.11-slim image.")
except DockerException as e:
    logger.error(f"Failed to initialize Docker executor: {e}")
    raise

# Define the CodeExecutorAgent for running code in a Docker container
code_executor_agent = CodeExecutorAgent(
    name="CodeExecutorAgent",
    description="Executes Python code in a secure Docker container.",
    code_executor=docker,
)
logger.info("CodeExecutorAgent initialized successfully.")

# Set up the RoundRobinGroupChat team with the two agents
team = RoundRobinGroupChat(
    participants=[problem_solver_expert, code_executor_agent],
    termination_condition=termination_condition,
    max_turns=15
)
logger.info("RoundRobinGroupChat team initialized with max 15 turns.")

# Main function to run the agent team and execute the task
async def run_code_executor_agent():
    try:
        # Start the Docker container
        logger.info("Starting Docker container...")
        await docker.start()

        # Define the task for solving the Rat in a Maze problem
        task = (
            "Write Python code to solve the Rat in a Maze problem using a backtracking algorithm. "
            "Generate a slow-moving GIF (using matplotlib and imageio) to visualize the solution path, "
            "ensuring the animation is slow enough to be clearly visible (e.g., 0.5 seconds per frame). "
            "Include three test cases: a solvable maze, an unsolvable maze, and an edge-case maze (e.g., 2x2). "
            "Save the output as `output.gif`."
        )
        logger.info("Task defined: %s", task)

        # Run the team task and stream messages
        async for message in team.run_stream(task=task):
            print("=" * 200)
            if isinstance(message, TextMessage):
                print(f"Message from: {message.source}")
                print(f"Content: {message.content}")
            elif isinstance(message, TaskResult):
                print(f"Stop reason: {message.stop_reason}")
            print("=" * 200)

    except DockerException as e:
        logger.error(f"Docker-related error: {e}")
        raise
    except Exception as e:
        logger.error(f"An error occurred during execution: {e}")
        raise
    finally:
        # Ensure Docker container is stopped to free resources
        logger.info("Stopping Docker container...")
        await docker.stop()

# Entry point for the script
if __name__ == "__main__":
    try:
        asyncio.run(run_code_executor_agent())
        logger.info("Code execution completed successfully.")
    except Exception as e:
        logger.error(f"Failed to run code executor agent: {e}")
    finally:
        print("Code execution completed.")