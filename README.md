# SnapShell

SnapShell is a powerful command-line utility designed to enhance your Linux terminal experience by auto-completing commands using a Language Learning Model (LLM). SnapShell intelligently suggests commands based on your input, maintains a history of suggested commands, and allows you to manage your command history with ease.

## Features

- **Smart Auto-completion**: Get AI-powered command suggestions based on what you're typing.
- **Command History**: Review previously suggested commands at any time.
- **History Management**: Clear the command history with a single command.
- **Database Update**: Easily update the database with the installed packages on your system.

## Installation

### Prerequisites
- Python 3.7 or higher
- `pip` package manager

### Installing via pip 
Install SnapShell with the following command:

```sh
pip install snapshell
```
### Custom Installation
SnapShell requires your Groq Api key during installation. Follow the on-screen instructions after installation

The installation will automatically detect your shell (bash, zsh, fish) and set the key in the respective configuration file.

OR

```sh
git clone https://github.com/KTS-o7/snapshell.git
cd snapshell
python -m venv env
source env/bin/activate
pip install -r requirements.txt
python setup.py install
```
## Dependencies

SnapShell requires the following libraries:

- `argparse`: For parsing command-line arguments.
- `sqlite3`: For local database operations.
- `os`: To interact with your operating system.

## Configuration Instructions
To use SnapShell, you need to set up the `HELPER_GROQ_API_KEY` environment variable. This is required for connecting to the underlying Language Model API.
### Setting the `HELPER_GROQ_API_KEY`
1. Obtain your API key from the GROQ service.
1. Set it as an environment variable:
```sh
export HELPER_GROQ_API_KEY="your_api_key_here"
```
Alternatively, you can add this to your shell's configuration file (`.bashrc`, `.zshrc`, etc.):
```sh
echo 'export HELPER_GROQ_API_KEY="your_api_key_here"' >> ~/.bashrc
```
Reload the shell configuration:
```sh
source ~/.bashrc
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
## Advanced Usage
You can chain arguments or integrate SnapShell with other terminal utilities for more advanced operations. Here's an example:
```sh
snapshell --update-db | grep "package-name"
```
## How It Works
SnapShell leverages a Language Learning Model to suggest relevant Linux commands based on user input. It keeps a local history of suggestions that can be reviewed or cleared at your discretion. Upon installation, SnapShell can update its internal database with packages installed on your system, ensuring up-to-date suggestions.

## Functions

- `view_history()`: Fetch and display the command history from the local database.
- `clear_history()`: Clear the command history in the local database.
- `main()`: The primary function that handles user input, command-line arguments, and interaction.

## API Documentation
SnapShell does not directly expose API endpoints, but it interacts with the GROQ API under the hood. Here’s a brief overview:
- **GROQ API Key**: Used to authenticate the SnapShell tool.
- **Command Suggestions**: SnapShell queries the GROQ API with the user's input to retrieve command suggestions in real-time.
If the project exposes new APIs in the future, detailed endpoint documentation should be added here.

## Contributing

We welcome contributions! If you'd like to contribute, please follow these steps: 
1. **Fork the repository**:Click the "Fork" button at the top of the GitHub repository page.
1. **Create a branch**: Create a new feature or bugfix branch.
```sh
git checkout -b feature/new-feature
```
3. **Code Style**: Follow PEP 8 guidelines for Python code.
4. **Testing**: Ensure your code passes all existing tests and add new tests if necessary.
5. **Submit a Pull Request**: Once your changes are ready, submit a pull request for review.

We currently need help to integrate SnapShell with more shells and support more platforms like windows.

## Troubleshooting
### Common Issues
1. **Installation Errors**: Ensure that you have the correct version of Python and pip installed. If dependencies fail to install, try updating pip:
```sh
pip install --upgrade pip
```
2. **Missing GROQ_API_KEY**: If SnapShell is not functioning properly, make sure the `HELPER_GROQ_API_KEY` is correctly set as an environment variable. You can check this by running:
```sh
echo $HELPER_GROQ_API_KEY
```
3. **Permission Denied**: If you encounter a "permission denied" error, try running the command with `sudo` or ensure you have the necessary file permissions.
4. **Clearing History Not Working**: If the history isn’t clearing, you might need to manually reset the SQLite database file used by SnapShell:
```sh
rm ~/.snapshell/history.db
```
If you encounter other issues, feel free to open an issue in the GitHub repository or contact us.
## License
SnapShell is licensed under the MIT License. For more details, see the LICENSE file.

## Contact

For any questions, issues, or feature requests, please reach out to:

**Krishnatejaswi S**  
[shentharkrishnatejaswi@gmail.com](mailto:shentharkrishnatejaswi@gmail.com)
