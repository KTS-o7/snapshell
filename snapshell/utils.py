
import sqlite3
import os
from .package_managers import detect_package_manager
from tqdm import tqdm


DB_PATH = os.path.expanduser('~/.snapshell/system_info.db')

# ANSI escape codes for colors
RESET = "\033[0m"
CYAN = "\033[36m"
GREEN = "\033[32m"
WHITE = "\033[37m"
BLUE = "\033[34m"
YELLOW = "\033[33m"
RED = "\033[31m"

def get_color(color:str):
    col = color.lower()
    if col == "cyan":
        return CYAN
    elif col == "green":
        return GREEN
    elif col == "white":
        return WHITE
    elif col == "blue":
        return BLUE
    elif col == "yellow":
        return YELLOW
    elif col == "red":
        return RED
    else:
        return RESET
    
def print_color(text, color:str):
    color = get_color(color)
    print(f"{color}{text}{RESET}")

def fetch_system_info():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT tool_name, version FROM system_config")
    system_info = cursor.fetchall()
    conn.close()

    package_manager = detect_package_manager()
    installed_packages = [{"name": pkg[0], "version": pkg[1]} for pkg in system_info]

    system_info_with_package_manager = {
        "installed_packages": installed_packages,
        "package_manager": package_manager.__class__.__name__
    }

    return system_info_with_package_manager

def create_database():
    if(os.path.exists(DB_PATH)):
        
        return
    print_color("Creating database...", "CYAN")
    os.makedirs(os.path.dirname(DB_PATH))
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS system_config (
            tool_name TEXT PRIMARY KEY,
            version TEXT,
            description TEXT,
            depends_on TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS command_suggestions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_input TEXT,
            command TEXT,
            explanation TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def update_database():
    create_database()
    print_color("Updating database...", "YELLOW")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    package_manager = detect_package_manager()
    installed_packages = package_manager.get_installed_packages()

    # Initialize the progress bar
    with tqdm(total=len(installed_packages), desc="Updating database", unit="pkg") as pbar:
        for package in installed_packages:
            cursor.execute('''
                INSERT OR REPLACE INTO system_config (tool_name, version, description, depends_on) 
                VALUES (?, ?, ?, ?)
            ''', (package['name'], package['version'], package.get('description', ''), ', '.join(package.get('depends_on', []))))
            pbar.update(1)  # Update the progress bar

    conn.commit()
    conn.close()
    print_color("Database updated successfully.", "GREEN")

def save_command_suggestion(user_input, command, explanation):
    create_database()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO command_suggestions (user_input, command, explanation)
        VALUES (?, ?, ?)
    ''', (user_input, command, explanation))
    conn.commit()
    conn.close()
    
def view_history():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT user_input, command, explanation, timestamp FROM command_suggestions ORDER BY timestamp DESC')
    results = cursor.fetchall()
    conn.close()

    if not results:
        print_color("No history found.", "YELLOW")
        return

    print_color("Command History:", "CYAN")
    for entry in results:
        user_input, command, explanation, timestamp = entry
        print_color(f"User Input: {user_input}", "GREEN")
        print_color(f"Command: {command}", "WHITE")
        print_color(f"Explanation: {explanation}", "BLUE")
        print_color(f"Timestamp: {timestamp}", "YELLOW")
        print("-" * 40)

def clear_history():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM command_suggestions')
    conn.commit()
    conn.close()
    print_color("Command history cleared successfully.", "GREEN")