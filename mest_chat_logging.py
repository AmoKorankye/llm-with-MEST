from openai import OpenAI
from dotenv import load_dotenv
import json
import uuid
import logging
from datetime import datetime
import os
from pathlib import Path

load_dotenv()

OPEN_AI_API_KEY = os.getenv("OPEN_AI_API_KEY")

LOG_FILE = "chatbot_logs.json"

def setup_logging():
    logger = logging.getLogger("Chatbot")
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(
            logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        )
        logger.addHandler(console_handler)

    # Ensure the log file exists and contains a valid JSON array
    if not Path(LOG_FILE).exists() or Path(LOG_FILE).stat().st_size == 0:
        with open(LOG_FILE, "w") as f:
            json.dump([], f)

    return logger


def save_log_entry(entry: dict):
    """Append a log entry while keeping the file as a valid JSON array"""
    try:
        with open(LOG_FILE, "r") as f:
            logs = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        logs = []

    logs.append(entry)

    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)

def initialize_client(use_ollama: bool = True) -> OpenAI:
    print(f"Initializing OpenAI client with Ollama: {use_ollama}")
    if use_ollama:
        return OpenAI(
            base_url="http://localhost:11434",
            api_key=OPEN_AI_API_KEY
        )
    else:
        return OpenAI(
            api_key=OPEN_AI_API_KEY
        )
        
        
class Chatbot:
    
    def __init__(self, use_ollama: bool = True):
        self.logger = setup_logging()
        self.session_id = str(uuid.uuid4())
        self.client = initialize_client(use_ollama)
        self.model_name = "gpt-4o-mini" if not use_ollama else "llama3.2:8b"
        
        self.messages = [{
            "role": "system",
            "content": "You are a helpful assistant that can answer questions and help with tasks."
        }]
        
    def chat(self, user_input: str) -> str:
        try:
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "level": "INFO",
                "type":"user_input",
                "metadata": {
                    "user_id": self.session_id,
                    "session_id": self.session_id,
                    "model": self.model_name
                }            
            }
        
            save_log_entry(log_entry)
            self.logger.info(json.dumps(log_entry))
            
            self.messages.append({
                "role": "user",
                "content": user_input
            })
            
            # Generate a response using the API
            start_time = datetime.now()
            response = self.client.chat.completions.create(
                model=self.model_name, messages=self.messages
            )
            
            end_time = datetime.now()
            
            # calculte the response time
            response_time = (end_time - start_time).total_seconds()
            
            # Extract the response from the AI
            assistant_response = response.choices[0].message.content
            
            # log the models response and performance metrics
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "level": "INFO",
                "type": "model_response",
                "model_response": assistant_response,
                "metadata": {
                    "session_id": self.session_id,
                    "model": self.model_name,
                    "response_time_seconds": response_time,
                    "tokens_used":(
                        # error here
                         response.usage.total_tokens
                         if hasattr(response, "usage") else None
                    )
                }
            }
            
            save_log_entry(log_entry)
            self.logger.info(json.dumps(log_entry))
            
            # append assistant's message to the conversation
            self.messages.append({
                "role": "assistant",
                "content": assistant_response
            })
        except Exception as e:
            # Log any erros that occur
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "level": "ERROR",
                "type": "error",
                "error_message": str(e),
                "metadata": {
                    "session_id": self.session_id,
                    "model": self.model_name,
                    "user_id": self.user_id
                }
            }
            
            save_log_entry(log_entry)
            self.logger.error(json.dumps(log_entry))
            return f"Sorry, something evil happened in the universe: {str(e)}" 
        
        return assistant_response
        
        
def main():
    # model selection
    print("\nSelect Model Type")
    print("1. OpenAI GPT-4")
    print("2. Ollama (Local)")
    
    while True:
        choice = input("Enter chouce (1 or 2): ").strip()
        if choice not in ["1", "2"]:
            print("Please enter either 1 or 2")
            break
    
        use_ollama = choice == "2"
        
        # initialize chat
        chatbot = Chatbot(use_ollama)
        
        print("\n=== Chat Session Started ===")
        print(f"Using {'Ollama' if use_ollama else 'OpenAI'} model")
        print("Type 'exit to end the conversations")
        print(f"Session ID: {chatbot.session_id}\n")
        
        while True:
            user_input = input("You: ").strip()
            
            if user_input.lower() == 'exit':
                print("\nGoodbye! ")
                break
            
            if not user_input:
                continue
            
            response = chatbot.chat(user_input)
            
            print(f"Bot: {response}\n")
            
            
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nChat Session ended by user. Goodbye!")