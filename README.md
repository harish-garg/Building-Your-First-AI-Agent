      # Simple Python AI Agent

This project is a simple, command-line AI agent built in Python. It demonstrates the core concepts of AI agentic workflows, including defining tools for a Large Language Model (LLM) and using it in a loop to accomplish tasks that require interaction with a local file system.

This agent can:
- List files in a directory.
- Read the content of files.
- Edit files by searching and replacing text.
- Run bash commands.

## Getting Started

Follow these instructions to set up and run the agent on your local machine.

### Prerequisites

- Python 3.7+
- `uv` (or `pip`) for package management. We recommend `uv` as it's extremely fast.

### Setup Instructions

1.  **Install `uv` (recommended):**
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # Create the virtual environment
    uv venv

    # Activate it (on macOS/Linux)
    source .venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    uv pip install anthropic
    ```

4.  **Set up your API Key:**
    This agent uses the Anthropic API. You'll need to get an API key from their website.

    Set the API key as an environment variable. On macOS or Linux, you can do this for your current terminal session like this:
    ```bash
    export ANTHROPIC_API_KEY="your-api-key-here"
    ```
    *Note: For a more permanent solution, add this line to your shell's startup file (e.g., `~/.zshrc` or `~/.bashrc`).*

## Usage

Once the setup is complete, you can run the agent with the following command:

```bash
python agent.py
    
