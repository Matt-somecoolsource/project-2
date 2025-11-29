import os
import google.generativeai as genai
from googleapiclient.discovery import build

# --- Configuration ---
try:
    GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
    SEARCH_ENGINE_ID = os.getenv("GOOGLE_CSE_ID")
    
    if not GEMINI_API_KEY or not SEARCH_ENGINE_ID:
        raise ValueError("API Key or Search Engine ID not found. Please set 'GOOGLE_API_KEY' and 'GOOGLE_CSE_ID' environment variables.")

    genai.configure(api_key=GEMINI_API_KEY)
    
except ValueError as e:
    print(f"Error: {e}")
    exit()

# --- Tool Definition: Web Search ---
def google_search(query: str) -> str:
    """Performs a Google search and returns a formatted string of results."""
    print(f"⚡ Performing MANUAL search for: '{query}'")
    try:
        service = build("customsearch", "v1", developerKey=GEMINI_API_KEY)
        res = service.cse().list(q=query, cx=SEARCH_ENGINE_ID, num=3).execute()
        
        if 'items' not in res or len(res['items']) == 0:
            return "No relevant search results found."

        snippets = [f"Title: {item.get('title', 'N/A')}\nSnippet: {item.get('snippet', 'N/A')}" for item in res['items']]
        return "\n\n".join(snippets)

    except Exception as e:
        print(f"An error occurred during search: {e}")
        return f"An error occurred during search: {e}"

# --- Agent Orchestration ---
tools = {
    'google_search': google_search
}

model = genai.GenerativeModel(
    model_name='gemini-2.5-flash',
    tools=list(tools.values())
)

# Start the chat WITHOUT automatic function calling. We will do it ourselves.
chat = model.start_chat()

print("🚀 AI Web Explorer [Manual Mode] is ready! Ask me anything. Type 'exit' to quit.")

# --- Main Interaction Loop ---
while True:
    try:
        user_question = input("\nYour question: ")
        if user_question.lower() == 'exit':
            print("Goodbye!")
            break

        # 1. Send the first message to the model
        response = chat.send_message(user_question)

        # 2. Check if the model wants to call a function
        if response.parts[0].function_call:
            # 3. It's an instruction! Execute it manually.
            function_call = response.parts[0].function_call
            function_name = function_call.name
            
            # Find the function to call in our 'tools' dictionary
            function_to_call = tools[function_name]
            
            # Extract arguments
            args = {key: value for key, value in function_call.args.items()}
            
            # Call the function
            function_response_text = function_to_call(**args)
            
            # 4. Send the search results back to the model
            response = chat.send_message(
                genai.protos.Part(
                    function_response=genai.protos.FunctionResponse(
                        name=function_name,
                        response={'result': function_response_text}
                    )
                )
            )
        
        # 5. Print the final text answer (this works for both simple and complex questions)
        print("\n💡 Agent's Answer:")
        print(response.text)

    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        print("Please try again.")
