import argparse
import sqlite3
from snapshell.utils import update_database, DB_PATH, print_color , clear_history, view_history
from .llm_api import LLMClient

def initial_setup(llm_client):
    # Prompt user for GROQ API key
    print_color("Please enter your GROQ API key:", "GREEN")
    groq_api_key = input("> " )
    
    # Set the API key
    llm_client.set_api_key(groq_api_key)
    
    print_color(f"Setting up the database... at {DB_PATH}", "YELLOW")
    llm_client.init_client()
    print_color("Database successfully created\n", "GREEN")
    print_color("Use the tool as snapshell\n", "GREEN")
    


def main():
    parser = argparse.ArgumentParser(description="Auto-complete Linux commands using an LLM.")
    parser.add_argument('--update-db', action='store_true', help="Update the database with installed packages")
    parser.add_argument('--view-history', action='store_true', help="View command history")
    parser.add_argument('--clear-history', action='store_true', help="Clear command history")
    parser.add_argument('--set-api-key', type=str, help="Set the GROQ API key")
    args = parser.parse_args()

    llm_client = LLMClient()

    if args.set_api_key:
        llm_client.set_api_key(args.set_api_key)
        print_color("API key set successfully.", "GREEN")
        return

    # Load the API key from the configuration file
    API_KEY = llm_client.load_api_key()

    if not API_KEY:
        initial_setup(llm_client)
    
    if args.update_db:
        print_color("Updating database...", "YELLOW")
        update_database()
        print_color("Database updated successfully.", "GREEN")

    if args.view_history:
        view_history()
        return

    if args.clear_history:
        clear_history()
        return
    
    print_color("Welcome to the SnapShell. Type 'exit' to quit.", "CYAN")
    
    llm_client.init_client()
    
    conversation_history = []
    
    while True:
        user_input = input(f"Enter your command query: ")

        if user_input.lower() == 'exit':
            print_color("Exiting the SnapShell. Goodbye!", "CYAN")
            break

        try:
            print_color("Fetching command suggestion...", "CYAN")
            suggestion = llm_client.suggest_command(user_input, conversation_history)
            print_color("Suggested Command:", "GREEN")
            print_color(suggestion.command, "WHITE")
            print_color("Explanation: \n", "BLUE")
            print_color(suggestion.explanation, "BLUE")
            print_color("Warning: This is a suggestion. Review and execute at your own risk.", "YELLOW")

            # Update conversation history
            conversation_history.append({"role": "user", "content": user_input})
            conversation_history.append({"role": "assistant", "content": suggestion.command})

            # Limit conversation history to the last 8 entries
            if len(conversation_history) > 16:
                conversation_history = conversation_history[-16:]

        except ValueError as e:
            print_color(str(e), "RED")
        print("-" * 40, "\n")

if __name__ == "__main__":
    main()