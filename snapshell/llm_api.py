# llm_api.py
import os
import json
import sqlite3
from groq import Groq
from pydantic import BaseModel, Field, ValidationError
from .package_managers import detect_package_manager
from .utils import DB_PATH, save_command_suggestion, fetch_system_info , update_database

# Configuration file path
CONFIG_FILE = os.path.expanduser("~/.snapshell_config.json")

# Data model for LLM to generate
class CommandSuggestion(BaseModel):
    command: str = Field(description="The suggested Linux command")
    explanation: str = Field(description="Explanation of the suggested command")

# Data model for SQL query validation
class SQLQuery(BaseModel):
    query: str = Field(description="The SQL query to be executed")

class LLMClient:
    def __init__(self):
        self.API_KEY = self.load_api_key()
        self.groq = None
        self.system_info = None
        self.package_manager = None

    def load_api_key(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as config_file:
                config = json.load(config_file)
            return config.get("GROQ_API_KEY")
        return None
    
    def init_client(self):
        self.groq = Groq(api_key=self.API_KEY)
        if(not os.path.exists(DB_PATH)):
            print("Database not found...\nCreating a new database. Please wait...")
            update_database()
        self.package_manager = detect_package_manager()
        self.system_info = fetch_system_info()

    def set_api_key(self, api_key):
        self.API_KEY = api_key
        config = {"GROQ_API_KEY": api_key}
        with open(CONFIG_FILE, "w") as config_file:
            json.dump(config, config_file)
        self.groq = Groq(api_key=self.API_KEY)

    def suggest_command(self, user_input, conversation_history):
        if not self.API_KEY:
            raise ValueError("API key not set. Please set the API key using set_api_key function.")        

        # Formulate SQL query using LLM
        sql_query = self.formulate_sql_query(user_input)

        # Validate the SQL query
        try:
            sql_query_model = SQLQuery(query=sql_query)
            sql_query = sql_query_model.query
        except ValidationError as e:
            # SQL query validation failed, proceed to fallback directly
            return self.fallback_to_llm(user_input,self.package_manager, "Failed to generate a valid SQL query. Interpreting your query directly.", conversation_history)

        # Query the database
        relevant_packages = self.query_database(sql_query)

        # Check if the database is empty or no results were found
        if not relevant_packages:
            # Database has no relevant packages, fall back to LLM interpretation
            return self.fallback_to_llm(user_input, self.package_manager, "No relevant packages found in the database.", conversation_history)

        # If relevant packages are found, format them for LLM
        relevant_packages_str = "\n".join([
            f"{pkg['name']}: {pkg['version']}, Description: {pkg.get('description', 'No description available')}"
            for pkg in relevant_packages
        ])

        system_prompt = (
            f"You are a helpful assistant that suggests Linux commands based on the following system info:\n"
            f"Relevant Installed Packages:\n{relevant_packages_str}\n"
            f"The package manager in use is {self.package_manager.__class__.__name__}. "
            "Please respond with a JSON object containing the suggested command and an explanation. "
            "Ensure the response is relevant to the user's query and provides accurate information."
        )

        messages = [
            {"role": "system", "content": system_prompt},
        ]

        # Add conversation history to messages
        messages.extend(conversation_history)

        messages.append({"role": "user", "content": user_input})

        chat_completion = self.groq.chat.completions.create(
            messages=messages,
            model="llama-3.2-90b-text-preview",
            temperature=0,
            stream=False,
            response_format={"type": "json_object"},
        )

        suggestion = CommandSuggestion.model_validate_json(chat_completion.choices[0].message.content)
        save_command_suggestion(user_input, suggestion.command, suggestion.explanation)
        return suggestion

    def fallback_to_llm(self, user_input, package_manager, fallback_message, conversation_history):
        """
        This function acts as a fallback to interpret the user query directly
        if SQL queries or database lookups don't provide relevant information.
        """
        system_prompt = (
            f"{fallback_message}\n"
            f"The package manager in use is {package_manager.__class__.__name__}. "
            "Please suggest the most appropriate Linux command based on the user's query, system information, and package manager."
            "Respond with a JSON object containing the suggested command and an explanation."
        )

        messages = [
            {"role": "system", "content": system_prompt},
        ]

        # Add conversation history to messages
        messages.extend(conversation_history)

        messages.append({"role": "user", "content": user_input})

        chat_completion = self.groq.chat.completions.create(
            messages=messages,
            model="llama-3.2-90b-text-preview",
            temperature=0,
            stream=False,
            response_format={"type": "json_object"},
        )

        suggestion = CommandSuggestion.model_validate_json(chat_completion.choices[0].message.content)
        save_command_suggestion(user_input, suggestion.command, suggestion.explanation)
        return suggestion

    def formulate_sql_query(self, user_input):
        system_prompt = (
        "You are a helpful assistant that generates SQL queries based on user input. "
        "Please generate a valid SQL query to fetch relevant packages from the system_config table. "
        "The SQL query should be in the following format: "
        "SELECT tool_name, version, description FROM system_config WHERE tool_name LIKE '%keyword%'; "
        "Replace 'keyword' with the relevant keyword from the user input. "
        "User input will be a natural language question with a command related to the system. Your query will help fetch the relevant packages. "
        "Output should be in JSON format."
    )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input},
        ]

        chat_completion = self.groq.chat.completions.create(
            messages=messages,
            model="llama-3.2-90b-text-preview",
            temperature=0,
            stream=False,
            response_format={"type": "json_object"},
        )

        llm_response = chat_completion.choices[0].message.content

        # Extract the SQL query from the LLM response using Pydantic model
        try:
            llm_response_model = SQLQuery.model_validate_json(llm_response)
            query = llm_response_model.query

        except ValidationError as e:
            query = ""

        return query

    def query_database(self, sql_query):
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute(sql_query)
            results = cursor.fetchmany(30)  # Fetch only the first 30 results
            conn.close()

            relevant_packages = [
                {
                    "name": pkg[0],
                    "version": pkg[1],
                    "description": pkg[2],
                }
                for pkg in results
            ]
            return relevant_packages
        except sqlite3.Error as e:
            # If there's any issue with the database query, return an empty result
            return []
