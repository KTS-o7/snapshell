# SnapShell

SnapShell is a powerful command-line utility designed to enhance your Linux terminal experience by auto-completing commands using a Language Learning Model (LLM). SnapShell intelligently suggests commands based on your input, maintains a history of suggested commands, and allows you to manage your command history with ease.

## Features

- **Smart Auto-completion**: Get AI-powered command suggestions based on what you're typing.
- **Command History**: Review previously suggested commands at any time.
- **History Management**: Clear the command history with a single command.
- **Database Update**: Easily update the database with the installed packages on your system.

## Installation

Install SnapShell via pip with the following command:

```sh
pip install snapshell
```

## Usage

Run SnapShell in your terminal using:

```sh
snapshell
```

### Command-line Arguments

SnapShell supports the following arguments:

- `--update-db`: Updates the database with currently installed packages.
- `--view-history`: Displays the command suggestion history.
- `--clear-history`: Clears all entries from the command history.

Example usage:

```sh
snapshell --update-db
snapshell --view-history
snapshell --clear-history
```

## Functions

- `view_history()`: Fetch and display the command history from the local database.
- `clear_history()`: Clear the command history in the local database.
- `main()`: The primary function that handles user input, command-line arguments, and interaction.

## Dependencies

SnapShell requires the following libraries:

- `argparse`: For parsing command-line arguments.
- `colorama`: For colorized terminal output.
- `sqlite3`: For local database operations.
- `os`: To interact with your operating system.

## How It Works

SnapShell leverages a Language Learning Model to suggest relevant Linux commands based on user input. It keeps a local history of suggestions that can be reviewed or cleared at your discretion. Upon installation, SnapShell can update its internal database with packages installed on your system, ensuring up-to-date suggestions.

## Custom Installation

SnapShell requires your GROQ API key during installation. Follow the on-screen instructions after installation

The installation will automatically detect your shell (bash, zsh, fish) and set the key in the respective configuration file.

OR

```bash
git clone https://github.com/KTS-o7/snapshell.git
cd snapshell
python -m venv env
source env/bin/activate
pip install -r requirements.txt
python setup.py install
```

## License

SnapShell is licensed under the MIT License. For more details, see the LICENSE file.

## Contributing

We welcome contributions! If you'd like to contribute, please open an issue or submit a pull request for any bug fixes or feature improvements.

We currently need help to integrate SnapShell with more shells and support more platforms like windows.

## Contact

For any questions, issues, or feature requests, please reach out to:

**Krishnatejaswi S**  
[shentharkrishnatejaswi@gmail.com](mailto:shentharkrishnatejaswi@gmail.com)
