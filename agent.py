import os
import json
import subprocess
from anthropic import Anthropic

# A library of tools the AI agent can use.
TOOL_LIBRARY = [
    {
        "name": "list_files",
        "description": "Get a list of all files and folders within a specified directory.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "The directory path to inspect (defaults to the current directory)."
                }
            }
        }
    },
    {
        "name": "read_file",
        "description": "Read the complete contents of a specified file.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "The path to the file to be read."
                }
            },
            "required": ["path"]
        }
    },
    {
        "name": "run_bash",
        "description": "Execute a bash command and return its standard output and error.",
        "input_schema": {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "The bash command to execute."
                }
            },
            "required": ["command"]
        }
    },
    {
        "name": "edit_file",
        "description": "Edit a file by replacing a specific string with a new one. Creates the file if it doesn't exist.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "The path to the file to be edited."
                },
                "search_string": {
                    "type": "string",
                    "description": "The text to search for. If empty, the file is created or overwritten."
                },
                "replace_string": {
                    "type": "string",
                    "description": "The text to replace the search_string with."
                }
            },
            "required": ["path", "search_string", "replace_string"]
        }
    }
]

def run_tool_command(name, arguments):
    """Executes a tool based on the provided name and arguments."""
    if name == "list_files":
        path = arguments.get("path", ".")
        files = os.listdir(path)
        return json.dumps(files, indent=2)
    
    elif name == "read_file":
        with open(arguments["path"], 'r') as f:
            return f.read()
    
    elif name == "run_bash":
        result = subprocess.run(
            arguments["command"],
            shell=True,
            capture_output=True,
            text=True
        )
        return f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
    
    elif name == "edit_file":
        path = arguments["path"]
        search_string = arguments["search_string"]
        replace_string = arguments["replace_string"]
        
        # If search_string is empty, create a new file or overwrite an existing one.
        if search_string == "":
            with open(path, 'w') as f:
                f.write(replace_string)
            return f"File '{path}' created/overwritten successfully."
        
        # Otherwise, perform a search and replace on an existing file.
        try:
            with open(path, 'r') as f:
                file_contents = f.read()
            
            new_contents = file_contents.replace(search_string, replace_string)
            
            with open(path, 'w') as f:
                f.write(new_contents)
            
            return f"File '{path}' edited successfully."
        except FileNotFoundError:
            return f"Error: File not found at path '{path}'."


def process_with_agent(user_request):
    """Runs the agent loop with a given user request."""
    client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    messages = [{"role": "user", "content": user_request}]
    
    print(f"\n🤖 Agent thinking about: '{user_request}'...")
    
    while True:
        # Call the model with the conversation history and the available tools.
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2048,
            messages=messages,
            tools=TOOL_LIBRARY
        )
        
        # Append the assistant's response to the message history.
        messages.append({"role": "assistant", "content": response.content})
        
        # Check if the model wants to use any tools.
        tool_calls = [c for c in response.content if c.type == "tool_use"]
        
        if not tool_calls:
            # If no tools are called, the agent is done. Print the final response.
            final_response = "".join([c.text for c in response.content if c.type == "text"])
            print(f"\n✅ Agent finished: {final_response}")
            break
        
        # If there are tool calls, execute them.
        tool_results = []
        for call in tool_calls:
            print(f"🔧 Using tool: '{call.name}' with input: {call.input}")
            result = run_tool_command(call.name, call.input)
            tool_results.append({
                "type": "tool_result",
                "tool_use_id": call.id,
                "content": str(result)
            })
        
        # Append the tool results to the conversation for the next turn.
        messages.append({"role": "user", "content": tool_results})


# Main interactive loop to run the agent from the command line.
if __name__ == "__main__":
    print("--- Simple Python AI Agent ---")
    while True:
        try:
            prompt = input("\n💬 What can I do for you? (Type 'quit' or 'exit' to end)\n> ")
            if prompt.lower() in ['quit', 'exit']:
                break
            process_with_agent(prompt)
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
