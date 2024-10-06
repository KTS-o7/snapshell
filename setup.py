from setuptools import setup, find_packages
from setuptools.command.install import install
import os
import colorama

DB_PATH = os.path.expanduser('~/.snapshell/system_info.db')

class CustomInstallCommand(install):
    def run(self):
        
        # Prompt user for GROQ API key
        colorama.init(autoreset=True)
        print(colorama.Fore.GREEN + "Please enter your GROQ API key:")
        groq_api_key = input(colorama.Fore.YELLOW + "> ")
        
        # Detect the user's shell
        user_shell = os.environ.get('SHELL', '/bin/bash')
        shell_config_file = {
            '/bin/bash': '~/.bashrc',
            '/bin/zsh': '~/.zshrc',
            '/bin/fish': '~/.config/fish/config.fish'
        }.get(user_shell)
        
        if shell_config_file:
            shell_config_path = os.path.expanduser(shell_config_file)
            
            # Set the GROQ API key in the user's shell config file
            with open(shell_config_path, "a") as shell_config:
                shell_config.write(f'\nexport HELPER_GROQ_API_KEY="{groq_api_key}"\n')
                print(colorama.Fore.GREEN + f"Added GROQ API key to {shell_config_path}")
            
            # Reload shell configuration
            os.system(f'source {shell_config_path}')
            from snapshell.database import create_database, update_database
            print(colorama.Fore.YELLOW + f"Setting up the database... at {DB_PATH}")
            create_database()
            install.run(self)
            update_database()
            
            print(colorama.Fore.GREEN + "Database successfully created\n")
            print(colorama.Fore.GREEN + "use the tool as snapshell\n")
            #restart the shell
            os.execvp(user_shell, [user_shell])
            
            
            
            
        else:
            print(f"Unrecognized shell: {user_shell}. Please manually add the following lines to your shell configuration file:")
            print(f'export HELPER_GROQ_API_KEY="{groq_api_key}"')

setup(
    name='snapshell',
    version='1.0.0',
    author='Krishnatejaswi S',
    author_email='shentharkrishnatejaswi@gmail.com',
    description='An AI-powered tool to suggest Linux commands based on user input',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/KTS-o7/snapshell',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'groq',
        'requests',
        'instructor',
        'pydantic',
        'colorama',
        'tqdm',  
    ],
    entry_points={
        'console_scripts': [
            'snapshell=snapshell.cli:main',
        ],
    },
    setup_requires=[
        'setuptools',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
    cmdclass={
        'install': CustomInstallCommand,
    },
)
