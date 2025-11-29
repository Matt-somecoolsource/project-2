import os
import requests
import json
from dotenv import load_dotenv

# --- Configuration ---
# Use override=True to FORCE the script to use the values from the .env file,
# ignoring any old or conflicting variables set in the terminal.
print("--- Loading environment variables from .env file (with override)...")
load_dotenv(override=True)

API_KEY = os.getenv("GOOGLE_API_KEY")
SEARCH_ENGINE_ID = os.getenv("GOOGLE_CSE_ID")

# --- SCRIPT DIAGNOSTICS ---
print("--- SCRIPT DIAGNOSTICS ---")
print(f"Value read for GOOGLE_API_KEY: {API_KEY}")
print(f"Value read for GOOGLE_CSE_ID: {SEARCH_ENGINE_ID}")
print("--------------------------")

# --- Validation ---
if not API_KEY or not SEARCH_ENGINE_ID:
    print("Error: Could not find environment variables. Is your .env file named correctly and in the right folder?")
    exit()

# The rest of the script remains the same...
search_query = "What are the latest advancements in AI?"
url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={search_query}"

try:
    print(f"🚀 Searching the web for: '{search_query}'...")
    response = requests.get(url)
    response.raise_for_status() 
    search_results = response.json()
    
    print("\n✅ Search complete. Here are the top results:\n")
    if 'items' in search_results and len(search_results['items']) > 0:
        for i, item in enumerate(search_results['items']):
            title = item.get('title', 'No Title')
            link = item.get('link', 'No Link')
            snippet = item.get('snippet', 'No Snippet').replace('\n', '')
            print(f"--- Result {i+1} ---\nTitle: {title}\nURL: {link}\nSnippet: {snippet}\n")
    else:
        print("No results found for your query.")

except requests.exceptions.RequestException as e:
    print(f"⚠️ An error occurred during the API request: {e}")
except Exception as e:
    print(f"⚠️ An unexpected error occurred: {e}")