# File: ai_brain.py

import google.generativeai as genai
import os

def setup_ai_brain():
    """Configures the Gemini API and returns the generative model."""
    try:
        api_key = os.environ["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        print("✅ Gemini API configured successfully.")
    except KeyError:
        # ... (error handling code remains the same)
        return None
    
    # 💡 THIS IS OUR FIX AND DIAGNOSTIC STEP
    model_name = 'gemini-pro-latest'
    print(f"💡 Attempting to use model: {model_name}") # <-- ADD THIS LINE
    model = genai.GenerativeModel(model_name)
    
    return model
    
    return model
def main():
    """Main function to run the AI interaction loop."""
    model = setup_ai_brain()
    if not model:
        return # Exit if setup failed

    print("\n🚀 Your AI Brain is ready. Ask me anything!")
    print("   (Type 'quit' or 'exit' to end the session)")

    while True:
        user_question = input("\nYour question: ")
        
        if user_question.lower() in ['quit', 'exit']:
            print("\nGoodbye! 👋")
            break
        
        if not user_question.strip():
            print("Please enter a question.")
            continue

        try:
            # Send the question to the Gemini model
            response = model.generate_content(user_question)

            # Print the model's response
            print("\n💡 AI Response:")
            print(response.text)

        except Exception as e:
            print(f"❌ An error occurred while generating a response: {e}")

if __name__ == "__main__":
    main()
