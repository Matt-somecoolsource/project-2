import os
import sys
import time
import threading
import itertools
import google.generativeai as genai
from googleapiclient.discovery import build

# --- UI Enhancements: Colors and Spinner ---
class Colors:
    """ANSI color codes for terminal output."""
    RESET = "\033[0m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    BOLD = "\033[1m"

class Spinner:
    """A context manager for showing a spinner in the terminal."""
    def __init__(self, message="Thinking..."):
        self.spinner = itertools.cycle(['-', '/', '|', '\\'])
        self.message = message
        self.done = False
        self.thread = None

    def spin(self):
        while not self.done:
            sys.stdout.write(f"\r{Colors.YELLOW}{self.message} {next(self.spinner)}{Colors.RESET}")
            sys.stdout.flush()
            time.sleep(0.1)

    def __enter__(self):
        self.done = False
        self.thread = threading.Thread(target=self.spin)
        self.thread.start()

    def __exit__(self, exc_type, exc_value, traceback):
        self.done = True
        self.thread.join()
        # Clear the spinner line
        sys.stdout.write('\r' + ' ' * (len(self.message) + 2) + '\r')
        sys.stdout.flush()

# --- Configuration ---
try:
    GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
    SEARCH_ENGINE_ID = os.getenv("GOOGLE_CSE_ID")
    
    if not GEMINI_API_KEY or not SEARCH_ENGINE_ID:
        raise ValueError("API Key or Search Engine ID not found. Please set 'GOOGLE_API_KEY' and 'GOOGLE_CSE_ID' environment variables.")

    genai.configure(api_key=GEMINI_API_KEY)
    
except ValueError as e:
    print(f"{Colors.RED}Error: {e}{Colors.RESET}")
    exit()

# --- Tool Definition: Web Search ---
def google_search(query: str) -> str:
    """Performs a Google search and returns a formatted string of results."""
    # This message will be hidden by the spinner, which is good UX
    try:
        service = build("customsearch", "v1", developerKey=GEMINI_API_KEY)
        res = service.cse().list(q=query, cx=SEARCH_ENGINE_ID, num=3).execute()
        
        if 'items' not in res or len(res['items']) == 0:
            return "No relevant search results found."

        snippets = [f"Title: {item.get('title', 'N/A')}\nSnippet: {item.get('snippet', 'N/A')}" for item in res['items']]
        return "\n\n".join(snippets)

    except Exception as e:
        return f"An error occurred during search: {e}"

# --- Agent Orchestration ---
tools = {'google_search': google_search}
model = genai.GenerativeModel(model_name='gemini-2.5-flash', tools=list(tools.values()))
chat = model.start_chat()

# --- Main Interaction Loop ---
def print_header():
    """Prints the application header."""
    print(f"{Colors.BOLD}{Colors.BLUE}🚀 AI Web Explorer is Ready!{Colors.RESET}")
    print("Ask me anything. Type 'exit' to quit.")
    print("-" * 40)

def main():
    """Main function to run the chat loop."""
    print_header()
    while True:
        try:
            user_question = input(f"\n{Colors.BOLD}{Colors.GREEN}Your question: {Colors.RESET}")
            if user_question.lower() == 'exit':
                print(f"\n{Colors.MAGENTA}Goodbye!{Colors.RESET}")
                break

            with Spinner("Thinking..."):
                response = chat.send_message(user_question)

            if response.parts[0].function_call:
                function_call = response.parts[0].function_call
                function_name = function_call.name
                
                if function_name in tools:
                    function_to_call = tools[function_name]
                    args = {key: value for key, value in function_call.args.items()}
                    
                    with Spinner(f"⚡ Searching the web for: '{args.get('query', '...')}'"):
                        function_response_text = function_to_call(**args)
                    
                    with Spinner("Summarizing findings..."):
                        response = chat.send_message(
                            genai.protos.Part(
                                function_response=genai.protos.FunctionResponse(
                                    name=function_name,
                                    response={'result': function_response_text}
                                )
                            )
                        )
            
            print(f"\n{Colors.BOLD}{Colors.CYAN}💡 Agent's Answer:{Colors.RESET}")
            # Simple formatting for the output
            for line in response.text.split('\n'):
                print(f"  {line}")
            print("-" * 40)

        except (KeyboardInterrupt, EOFError):
            print(f"\n{Colors.MAGENTA}Goodbye!{Colors.RESET}")
            break
        except Exception as e:
            print(f"\n{Colors.RED}An unexpected error occurred: {e}{Colors.RESET}")
            print("Please try again.")

if __name__ == "__main__":
    main()
