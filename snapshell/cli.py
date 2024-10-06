import argparse
from colorama import Fore, Style, init
from .llm_api import suggest_command
from .database import update_database, DB_PATH
import sqlite3
import os

init(autoreset=True)  # Initialize colorama

def view_history():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT user_input, command, explanation, timestamp FROM command_suggestions ORDER BY timestamp DESC')
    results = cursor.fetchall()
    conn.close()

    if not results:
        print(f"{Fore.YELLOW}No history found.{Style.RESET_ALL}")
        return

    print(f"{Fore.CYAN}Command History:{Style.RESET_ALL}")
    for entry in results:
        user_input, command, explanation, timestamp = entry
        print(f"{Fore.GREEN}User Input: {user_input}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Command: {command}{Style.RESET_ALL}")
        print(f"{Fore.BLUE}Explanation: {explanation}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Timestamp: {timestamp}{Style.RESET_ALL}")
        print("-" * 40)

def clear_history():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM command_suggestions')
    conn.commit()
    conn.close()
    print(f"{Fore.GREEN}Command history cleared successfully.{Style.RESET_ALL}")

def main():
    parser = argparse.ArgumentParser(description="Auto-complete Linux commands using an LLM.")
    parser.add_argument('--update-db', action='store_true', help="Update the database with installed packages")
    parser.add_argument('--view-history', action='store_true', help="View command history")
    parser.add_argument('--clear-history', action='store_true', help="Clear command history")
    args = parser.parse_args()

    if args.update_db:
        print(f"{Fore.YELLOW}Updating database...{Style.RESET_ALL}")
        update_database()
        print(f"{Fore.GREEN}Database updated successfully.{Style.RESET_ALL}")

    if args.view_history:
        view_history()
        return

    if args.clear_history:
        clear_history()
        return

    print(f"{Fore.CYAN}Welcome to the Linux Command Tool. Type 'exit' to quit.{Style.RESET_ALL}")

    conversation_history = []

    while True:
        user_input = input(f"{Fore.CYAN}Enter your command query: {Style.RESET_ALL}")

        if user_input.lower() == 'exit':
            print(f"{Fore.CYAN}Exiting the Linux Command Tool. Goodbye!{Style.RESET_ALL}")
            break

        try:
            print(f"{Fore.CYAN}Fetching command suggestion...{Style.RESET_ALL}")
            suggestion = suggest_command(user_input, conversation_history)
            print(f"{Fore.GREEN}Suggested Command: \n {Style.RESET_ALL}")
            print(f"{Fore.WHITE}{suggestion.command}{Style.RESET_ALL}\n")
            print(f"{Fore.BLUE}Explanation: {suggestion.explanation}{Style.RESET_ALL}\n")
            print(f"{Fore.YELLOW}Warning: This is a suggestion. Review and execute at your own risk.{Style.RESET_ALL}")

            # Update conversation history
            conversation_history.append({"role": "user", "content": user_input})
            conversation_history.append({"role": "assistant", "content": suggestion.command})

            # Limit conversation history to the last 8 entries
            if len(conversation_history) > 16:
                conversation_history = conversation_history[-16:]

        except ValueError as e:
            print(f"{Fore.RED}{e}{Style.RESET_ALL}")
        print("-" * 40,"\n")

if __name__ == "__main__":
    main()