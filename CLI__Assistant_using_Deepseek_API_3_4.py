# CLI Assistant using DeepSeek Official API
# Uses environment variables for API keys

import os
from openai import OpenAI
from colorama import Fore, init
import requests
import json

# Initialize colorama
init(autoreset=True)

class CLIAssistant:
    def __init__(self):
        # Get API key from environment variable
        api_key = "sk-459e319768154a98b65306dad2052efc"
        if not api_key:
            raise ValueError("DEEPSEEK_API_KEY environment variable not set!")
        
        # Use DeepSeek's official API endpoint
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com"  # Official DeepSeek API
        )
        self.conversation_history = [
            {"role": "system", "content": "You are a helpful CLI assistant. Be concise."}
        ]

    def clear_history(self):
        # Clear and reset the conversation history
        self.conversation_history = [
            {"role": "system", "content": "You are a helpful CLI assistant. Be concise."}
        ]

    def get_response(self, user_input, stream=False):
        # Get AI response for user input
        self.conversation_history.append({"role": "user", "content": user_input})
        
        if stream:
            return self._get_streaming_response()
        else:
            return self._get_standard_response()

    def _get_standard_response(self):
        try:
            response = self.client.chat.completions.create(
                model="deepseek-chat",  # Official DeepSeek model
                messages=self.conversation_history,
                stream=False
            )
            
            ai_response = response.choices[0].message.content
            self.conversation_history.append({"role": "assistant", "content": ai_response})
            return ai_response
        except Exception as e:
            return f"API Error: {str(e)}"

    def _get_streaming_response(self):
        # Get streaming AI response
        print(f"{Fore.YELLOW}Assistant: ", end="", flush=True)
        
        try:
            response = self.client.chat.completions.create(
                model="deepseek-chat",  # Official DeepSeek model
                messages=self.conversation_history,
                stream=True
            )
            
            full_response = ""
            for chunk in response:
                if chunk.choices[0].delta.content:
                    chunk_text = chunk.choices[0].delta.content
                    print(chunk_text, end="", flush=True)
                    full_response += chunk_text
            
            print()  # New line after streaming
            self.conversation_history.append({"role": "assistant", "content": full_response})
            return full_response
        except Exception as e:
            return f"API Error: {str(e)}"

    def process_command(self, user_input):
        # Handle special commands or normal queries
        if user_input.lower() in ["exit", "quit"]:
            return None, True  # Exit command
        
        elif user_input.lower() in ["clear", "reset"]:
            self.clear_history()
            return "Conversation history cleared.", False
        
        elif user_input.lower().startswith("save "):
            filename = user_input[5:].strip()
            return self._save_conversation(filename), False
        
        elif user_input.lower().startswith("load "):
            filename = user_input[5:].strip()
            return self._load_conversation(filename), False
        
        elif user_input.lower().startswith("file "):
            filename = user_input[5:].strip()
            return self._process_file(filename), False
        
        elif user_input.lower().startswith("stream "):
            query = user_input[7:].strip()
            response = self.get_response(query, stream=True)
            return response, False
        
        elif user_input.lower() in ["help", "commands"]:
            return self._show_help(), False
        
        elif user_input.lower() == "models":
            return self._list_models(), False
        
        # Normal query
        response = self.get_response(user_input, stream=False)
        return response, False

    def _save_conversation(self, filename):
        # Save conversation to file
        try:
            with open(filename, 'w') as f:
                for msg in self.conversation_history:
                    f.write(f"{msg['role']}: {msg['content']}\n")
            return f"Conversation saved to {filename}."
        except Exception as e:
            return f"Error saving conversation: {str(e)}"

    def _load_conversation(self, filename):
        # Load conversation from file
        try:
            with open(filename, "r") as f:
                lines = f.readlines()
                self.clear_history()
                
                for line in lines:
                    line = line.strip()
                    if not line:
                        continue
                    
                    if ": " not in line:
                        print(f"Skipping malformed line: {line}")
                        continue
                    
                    role, content = line.split(": ", 1)
                    role = role.strip().lower()
                    
                    # Validate role
                    if role not in ["system", "user", "assistant"]:
                        print(f"Warning: Invalid role '{role}' in file, treating as 'user'")
                        role = "user"
                    
                    self.conversation_history.append({"role": role, "content": content.strip()})
                
                return f"Conversation loaded from {filename}"
        except FileNotFoundError:
            return f"Error: File '{filename}' not found."
        except Exception as e:
            return f"Error loading conversation: {str(e)}"

    def _process_file(self, filename):
        # Process the contents of a file
        try:
            with open(filename, 'r') as f:
                content = f.read()
                response = self.get_response(f"Process this file content: \n{content}", stream=False)
                return response
        except FileNotFoundError:
            return f"Error: File '{filename}' not found."
        except Exception as e:
            return f"Error processing file: {str(e)}"

    def _list_models(self):
        # List available models (optional feature)
        try:
            models = self.client.models.list()
            model_list = [model.id for model in models.data]
            return f"Available models:\n" + "\n".join(f"- {model}" for model in model_list)
        except Exception as e:
            return f"Could not fetch models: {str(e)}"

    def _show_help(self):
        # Show available commands
        return """Available commands:
- `exit` or `quit`: Exit the assistant.
- `clear` or `reset`: Clear the conversation history.
- `help` or `commands`: Show this help message.
- `save <filename>`: Save the conversation to a file.
- `load <filename>`: Load a conversation from a file.
- `file <filename>`: Process the contents of a file.
- `stream <query>`: Get streaming response for query.
- `models`: List available models (if supported).
"""

def main():
    try:
        assistant = CLIAssistant()
        print(f"{Fore.YELLOW}CLI Assistant initialized. Type 'help' for commands.")
        print(f"{Fore.YELLOW}Using DeepSeek Official API")
        
        while True:
            try:
                user_input = input(f"{Fore.CYAN}\nUser: ").strip()
                
                if not user_input:
                    continue
                
                response, should_exit = assistant.process_command(user_input)
                
                if should_exit:
                    print(f"{Fore.YELLOW}Goodbye!")
                    break
                
                if response and not user_input.startswith("stream "):
                    print(f"{Fore.GREEN}{response}")
                    
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}Use 'exit' or 'quit' to exit the session.")
            except Exception as e:
                print(f"{Fore.RED}Error: {str(e)}")
    
    except ValueError as e:
        print(f"{Fore.RED}Initialization Error: {str(e)}")
        print(f"{Fore.YELLOW}Please set your API key:")
        print(f"{Fore.YELLOW}Linux/Mac: export DEEPSEEK_API_KEY='your-api-key'")
        print(f"{Fore.YELLOW}Windows: set DEEPSEEK_API_KEY=your-api-key")

if __name__ == "__main__":
    main()