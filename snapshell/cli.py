import argparse
import os
import sqlite3
from snapshell.database import create_database, update_database, DB_PATH
from .llm_api import suggest_command, set_api_key, load_api_key

# ANSI escape codes for colors
RESET = "\033[0m"
CYAN = "\033[36m"
GREEN = "\033[32m"
WHITE = "\033[37m"
BLUE = "\033[34m"
YELLOW = "\033[33m"
RED = "\033[31m"

def initial_setup():
    # Prompt user for GROQ API key
    print(GREEN + "Please enter your GROQ API key:" + RESET)
    groq_api_key = input(YELLOW + "> " + RESET)
    
    # Set the API key
    set_api_key(groq_api_key)
    
    print(YELLOW + f"Setting up the database... at {DB_PATH}" + RESET)
    create_database()
    update_database()
    print(GREEN + "Database successfully created\n" + RESET)
    print(GREEN + "Use the tool as snapshell\n" + RESET)

def view_history():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT user_input, command, explanation, timestamp FROM command_suggestions ORDER BY timestamp DESC')
    results = cursor.fetchall()
    conn.close()

    if not results:
        print(f"{YELLOW}No history found.{RESET}")
        return

    print(f"{CYAN}Command History:{RESET}")
    for entry in results:
        user_input, command, explanation, timestamp = entry
        print(f"{GREEN}User Input: {user_input}{RESET}")
        print(f"{WHITE}Command: {command}{RESET}")
        print(f"{BLUE}Explanation: {explanation}{RESET}")
        print(f"{YELLOW}Timestamp: {timestamp}{RESET}")
        print("-" * 40)

def clear_history():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM command_suggestions')
    conn.commit()
    conn.close()
    print(f"{GREEN}Command history cleared successfully.{RESET}")

def main():
    parser = argparse.ArgumentParser(description="Auto-complete Linux commands using an LLM.")
    parser.add_argument('--update-db', action='store_true', help="Update the database with installed packages")
    parser.add_argument('--view-history', action='store_true', help="View command history")
    parser.add_argument('--clear-history', action='store_true', help="Clear command history")
    parser.add_argument('--set-api-key', type=str, help="Set the GROQ API key")
    args = parser.parse_args()

    if args.set_api_key:
        set_api_key(args.set_api_key)
        print(GREEN + "API key set successfully." + RESET)
        return

    # Load the API key from the configuration file
    API_KEY =  load_api_key()


    if not API_KEY:
        print("This is working")
        initial_setup()
    
    if args.update_db:
        print(f"{YELLOW}Updating database...{RESET}")
        update_database()
        print(f"{GREEN}Database updated successfully.{RESET}")

    if args.view_history:
        view_history()
        return

    if args.clear_history:
        clear_history()
        return
    
    print(f"{CYAN}Welcome to the Linux Command Tool. Type 'exit' to quit.{RESET}")

    conversation_history = []

    while True:
        user_input = input(f"{CYAN}Enter your command query: {RESET}")

        if user_input.lower() == 'exit':
            print(f"{CYAN}Exiting the Linux Command Tool. Goodbye!{RESET}")
            break

        try:
            print(f"{CYAN}Fetching command suggestion...{RESET}")
            suggestion = suggest_command(user_input, conversation_history)
            print(f"{GREEN}Suggested Command: \n {RESET}")
            print(f"{WHITE}{suggestion.command}{RESET}\n")
            print(f"{BLUE}Explanation: {suggestion.explanation}{RESET}\n")
            print(f"{YELLOW}Warning: This is a suggestion. Review and execute at your own risk.{RESET}")

            # Update conversation history
            conversation_history.append({"role": "user", "content": user_input})
            conversation_history.append({"role": "assistant", "content": suggestion.command})

            # Limit conversation history to the last 8 entries
            if len(conversation_history) > 16:
                conversation_history = conversation_history[-16:]

        except ValueError as e:
            print(f"{RED}{e}{RESET}")
        print("-" * 40,"\n")

if __name__ == "__main__":
    main()