DSA Solver
A Streamlit-based application for solving Data Structures and Algorithms (DSA) problems using the Autogen framework with Docker-based execution.
Overview
The DSA Solver allows users to input DSA problems (e.g., "Find the sum of two numbers") via a web interface. It leverages Autogen's agent-based framework to process the problem, execute code in a Docker container, and display results in a chat-like UI.
Features

Interactive UI: Built with Streamlit for easy problem input and result visualization.
Autogen Integration: Uses Autogen agents (ProblemSolverExpert, CodeExecutorAgent) to solve and execute DSA problems.
Docker Execution: Runs code in isolated Docker containers for security and consistency.
Chat-like Output: Displays responses from different agents with avatars for clarity.

Project Structure
dsa-solver/
│
├── app.py                  # Main Streamlit application
├── main.py                 # Autogen team and task logic
├── config/
│   ├── docker_utils.py     # Docker executor utilities
│   ├── model_client.py     # Model client configuration
├── requirements.txt         # Project dependencies
├── README.md               # Project documentation

Setup Instructions

Clone the Repository:
git clone <repository-url>
cd dsa-solver


Install Dependencies:Ensure Python 3.8+ is installed, then run:
pip install -r requirements.txt


Run the Application:
streamlit run app.py


Dependencies:

Streamlit
Autogen-AgentChat
Docker (ensure Docker is running)
Other dependencies listed in requirements.txt



Usage

Open the app in your browser (typically http://localhost:8501).
Enter a DSA question in the text input (e.g., "Can you give me a solution to add 2 numbers?").
Click the "Solve" button to process the question.
View the results in the chat-like interface, with responses from ProblemSolverExpert (solution explanation) and CodeExecutorAgent (code execution).

Development

Adding New Features: Extend main.py for new Autogen agents or modify app.py for UI enhancements.
Testing: Ensure Docker is running before testing. Add unit tests in a tests/ directory for robustness.
Contributing: Submit pull requests with clear descriptions of changes.

Known Issues

Asyncio event loop conflicts with Streamlit; mitigated by proper async handling.
Limited error feedback in the UI; ongoing improvements to display detailed errors.

Future Improvements

Add problem history and reset functionality.
Support for multiple programming languages in code execution.
Enhanced error handling and user feedback.

Contact
For questions, contact Furquan at .