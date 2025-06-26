import asyncio
import os
from typing import Optional, Dict
from dotenv import load_dotenv
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.tools import FunctionTool
import httpx
from bs4 import BeautifulSoup
import html2text
from urllib.parse import urljoin

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set.")

# Initialize the OpenAI model client
openai_client = OpenAIChatCompletionClient(model="gpt-4o-mini", api_key=api_key)

# Define custom functions
def reverse_string(text: str) -> str:
    """Reverse the given text string.
    
    Args:
        text: The input string to reverse.
    
    Returns:
        str: The reversed string.
    
    Example:
        Input: "Hello, World!" -> Output: "!dlroW ,olleH"
    """
    return text[::-1]

def summarize_text(text: str, max_length: int = 100) -> str:
    """Summarize a text by truncating it to a specified length.
    
    Args:
        text: The input text to summarize.
        max_length: Maximum length of the summary (default: 100 characters).
    
    Returns:
        str: The summarized text, truncated to max_length with '...' appended if truncated.
    
    Example:
        Input: "This is a long text about AI.", max_length=20
        Output: "This is a long text..."
    """
    if len(text) <= max_length:
        return text
    return text[:max_length].rsplit(" ", 1)[0] + "..."

def read_text_file(file_path: str) -> str:
    """Read the contents of a text file.
    
    Args:
        file_path: Path to the text file to read.
    
    Returns:
        str: The contents of the file.
    
    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file is not a text file.
    
    Example:
        Input: "data.txt" (containing "Hello from file!")
        Output: "Hello from file!"
    """
    if not file_path.endswith((".txt", ".md")):
        raise ValueError("Only .txt and .md files are supported.")
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")

def calculate_expression(expression: str) -> float:
    """Evaluate a basic arithmetic expression.
    
    Args:
        expression: A string containing a basic arithmetic expression (e.g., '2 + 3 * 4').
    
    Returns:
        float: The result of the evaluated expression.
    
    Raises:
        ValueError: If the expression is invalid.
    
    Example:
        Input: "2 + 3 * 4"
        Output: 14.0
    """
    try:
        allowed_chars = set("0123456789 +-*/.()")
        if not all(c in allowed_chars for c in expression):
            raise ValueError("Invalid characters in expression.")
        result = eval(expression, {"__builtins__": {}})  # Disable built-ins for safety
        return float(result)
    except Exception as e:
        raise ValueError(f"Invalid expression: {str(e)}")

async def fetch_webpage(url: str, include_images: bool = True, max_length: Optional[int] = None) -> str:
    """Fetch a webpage and convert it to markdown format.
    
    Args:
        url: The URL of the webpage to fetch.
        include_images: Whether to include image references in the markdown (default: True).
        max_length: Maximum length of the output markdown (if None, no limit).
    
    Returns:
        str: Markdown version of the webpage content.
    
    Raises:
        ValueError: If the URL is invalid or the page can't be fetched.
    
    Example:
        Input: "https://example.com", include_images=False, max_length=100
        Output: Markdown content of the webpage, truncated to 100 characters.
    """
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            for script in soup(["script", "style"]):
                script.decompose()
            for tag in soup.find_all(["a", "img"]):
                if tag.get("href"):
                    tag["href"] = urljoin(url, tag["href"])
                if tag.get("src"):
                    tag["src"] = urljoin(url, tag["src"])

            h2t = html2text.HTML2Text()
            h2t.body_width = 0
            h2t.ignore_images = not include_images
            h2t.ignore_emphasis = False
            h2t.ignore_links = False
            markdown = h2t.handle(str(soup))

            if max_length and len(markdown) > max_length:
                markdown = markdown[:max_length].rsplit(" ", 1)[0] + "..."
            return markdown.strip()

    except httpx.RequestError as e:
        raise ValueError(f"Failed to fetch webpage: {str(e)}")
    except Exception as e:
        raise ValueError(f"Error processing webpage: {str(e)}")

# Register tools
reverse_tool = FunctionTool(
    reverse_string,
    description="Reverses the order of characters in a given text string."
)
summarize_tool = FunctionTool(
    summarize_text,
    description="Summarizes a given text to a specified length by truncating it."
)
file_read_tool = FunctionTool(
    read_text_file,
    description="Reads the contents of a text file (.txt or .md) and returns them as a string."
)
calc_tool = FunctionTool(
    calculate_expression,
    description="Evaluates a basic arithmetic expression (e.g., '2 + 3 * 4')."
)
fetch_webpage_tool = FunctionTool(
    fetch_webpage,
    description="Fetches a webpage and converts its content to markdown format."
)

# Create agent
agent = AssistantAgent(
    name="MultiToolAgent",
    model_client=openai_client,
    system_message="You are a helpful assistant that can reverse text, summarize text, read files, perform calculations, and fetch webpages using the provided tools.",
    tools=[reverse_tool, summarize_tool, file_read_tool, calc_tool, fetch_webpage_tool],
    reflect_on_tool_use=True,
)

# Define a task
task = "Calculate the result of '5 + 6 * 2' and then reverse the result."

# Run the agent
async def main():
    try:
        result = await agent.run(task=task)
        print(f"Agent Response: {result.messages[-1].content}")
    except Exception as e:
        print(f"Error running agent: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())