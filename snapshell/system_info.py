import sqlite3
from .database import DB_PATH
from .package_managers import detect_package_manager

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