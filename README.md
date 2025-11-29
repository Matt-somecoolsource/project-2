# project-2
# 🚀 AI Web Explorer: Your Smart Research Bot

This project is an intelligent AI agent that acts as a personal research assistant. It uses Google's Gemini model and Google's Custom Search API to find, process, and summarize information from the internet in response to a user's question.

## ✨ Core Features

- **Natural Language Queries:** Ask questions in plain English.
- **Live Web Search:** The agent automatically searches the web for the most relevant and up-to-date information.
- **AI-Powered Summarization:** It intelligently synthesizes the information found into a concise, easy-to-understand answer.
- **Interactive CLI:** A clean and user-friendly command-line interface with status indicators and colored output for clarity.

## 🛠️ Technology Stack

- **Language:** Python 3
- **AI Model:** Google Gemini (`gemini-1.5-flash`)
- **Core Libraries:**
    - `google-generativeai`: For interacting with the Gemini API.
    - `google-api-python-client`: For using the Google Custom Search API.

## ⚙️ Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd <your-repo-directory>
    ```

2.  **Install dependencies:**
    ```bash
    pip install google-generativeai google-api-python-client
    ```

3.  **Configure Environment Variables:**
    You need to set up two environment variables with your API keys.

    *On macOS/Linux:*
    ```bash
    export GOOGLE_API_KEY="YOUR_GEMINI_API_KEY"
    export GOOGLE_CSE_ID="YOUR_CUSTOM_SEARCH_ENGINE_ID"
    ```

    *On Windows (Command Prompt):*
    ```bash
    set GOOGLE_API_KEY="YOUR_GEMINI_API_KEY"
    set GOOGLE_CSE_ID="YOUR_CUSTOM_SEARCH_ENGINE_ID"
    ```

## 🏃 How to Run

Once the setup is complete, run the bot from your terminal:

```bash
python your_script_name.py
