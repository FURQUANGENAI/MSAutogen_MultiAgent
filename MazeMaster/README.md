MazeMaster: Rat in a Maze Solver with Autogen and Docker

Overview
MazeMaster is a multi-agent system built with Autogen 0.6.1 to solve the Rat in a Maze problem using a backtracking algorithm and generate a slow-moving GIF visualization. The system leverages two agents running in a Docker container for secure code execution, making it robust and reproducible.

Key Features
Problem Solving: Solves the Rat in a Maze problem using a backtracking algorithm.
Visualization: Generates a slow-moving GIF (output.gif) with a 0.5-second delay per frame using matplotlib and imageio.
Test Cases: Includes three test cases: solvable maze, unsolvable maze, and edge-case (e.g., 2x2 maze).
Docker Integration: Executes code in a secure python:3.11-slim Docker container.
Error Handling: Handles missing dependencies and code errors, with detailed logging.
Asynchronous Execution: Uses asyncio for efficient agent communication.

Prerequisites
Python: Version 3.11 or higher.
Docker Desktop: Installed and running on Windows (with WSL 2 or Hyper-V backend).
OpenAI API Key: Required for GPT-4o-mini model access.
Windows: The project is tested on Windows 10/11, but it should work on other platforms with minor adjustments.

Setup Instructions
1. Clone the Repository
Clone or copy the project to your local machine:
cd C:\AutogenWorkspace
mkdir MazeMaster
cd MazeMaster

Place autogen_docker_llm_multiagent.py and requirements.txt in C:\AutogenWorkspace\MazeMaster.
2. Set Up Virtual Environment
Create and activate a Python virtual environment:
python -m venv autogen-lc
.\autogen-lc\Scripts\activate

3. Install Dependencies
Install the required Python packages listed in requirements.txt:
pip install -r requirements.txt

requirements.txt:
autogen-agentchat==0.6.1
autogen-ext[docker]==0.6.1
python-dotenv==1.0.1
docker==7.1.0
openai==1.51.0
asyncio_atexit==1.0.1
# Optional dependencies for GIF generation (if needed in host environment)
# matplotlib==3.9.2
# imageio==2.36.0

4. Configure Docker
Install Docker Desktop: Download and install from Docker’s official website. Use WSL 2 backend for Windows 10/11 Pro or Enterprise.
Start Docker Desktop: Ensure it’s running (check the system tray icon).
Verify Docker: Run docker info to confirm the daemon is accessible.
Pull Python Image: Pull the python:3.11-slim image:docker pull python:3.11-slim


Optional Custom Image: To pre-install matplotlib and imageio, create a Dockerfile:FROM python:3.11-slim
RUN apt-get update && apt-get install -y libx11-6
RUN pip install matplotlib==3.9.2 imageio==2.36.0

Build it:docker build -t custom-python:3.11-slim .

Update autogen_docker_llm_multiagent.py to use image="custom-python:3.11-slim".

5. Set Up Environment Variables
Create a .env file in C:\AutogenWorkspace\MazeMaster with your OpenAI API key:
echo OPENAI_API_KEY=your_api_key_here > .env

Replace your_api_key_here with your valid OpenAI API key.
6. Create Working Directory
Create the tmp directory for Docker file outputs:
mkdir C:\AutogenWorkspace\MazeMaster\tmp

Usage
Run the script to solve the Rat in a Maze problem and generate a GIF:
cd C:\AutogenWorkspace\MazeMaster
.\autogen-lc\Scripts\activate
python autogen_docker_llm_multiagent.py


Windows Note: If you encounter a Docker error (e.g., “Error while fetching server API version”), ensure Docker Desktop is running and run the terminal as Administrator. Optionally, set the Docker host:os.environ["DOCKER_HOST"] = "npipe:////./pipe/docker_engine"

Add this line after load_dotenv() in the script.

Output

Console Output: Printed to the terminal, including:
Logging messages (e.g., “OpenAI client initialized successfully”).
Agent messages from ProblemSolverExpert (problem explanation, Python code, test case outputs) and CodeExecutorAgent (execution results).
Final “STOP” message and stop reason.
Save to a file (optional):python autogen_docker_llm_multiagent.py > output.log




GIF Output: Saved as C:\AutogenWorkspace\MazeMaster\tmp\output.gif:
Visualizes the rat’s path through the maze with a 0.5-second delay per frame.
Open with Windows Photos, a browser, or VLC Media Player.



Project Structure
MazeMaster/
├── autogen_docker_llm_multiagent.py  # Main script
├── requirements.txt                  # Python dependencies
├── .env                             # Environment variables (create manually)
├── tmp/                             # Working directory for Docker outputs
│   └── output.gif                   # Generated GIF
└── output.log                       # Optional console output log

Troubleshooting

Docker Error: If you see “Error while fetching server API version”:
Ensure Docker Desktop is running.
Run docker info to verify the daemon.
Add user to docker-users group: net localgroup docker-users <your-username> /add.
Set DOCKER_HOST as described above.


Missing GIF: If tmp/output.gif is missing, check console output for errors. Ensure the Docker container has matplotlib and imageio (use custom image if needed).
API Key Error: Verify OPENAI_API_KEY in .env is valid.
Dependencies: Reinstall requirements.txt if errors persist:pip install -r requirements.txt



Next Steps

Test with larger mazes or additional DSA problems.
Optimize GIF generation for performance.
Document Windows-specific Docker setup for team members.

Acknowledgments

Built with Autogen 0.6.1 and Docker.
