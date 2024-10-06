# database.py
import sqlite3
import os
from .package_managers import detect_package_manager
from tqdm import tqdm

DB_PATH = os.path.expanduser('~/.snapshell/system_info.db')

def create_database():
    if not os.path.exists(os.path.dirname(DB_PATH)):
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