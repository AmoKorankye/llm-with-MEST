import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Get API key from environment
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("Error: OPENAI_API_KEY not found in .env file")
    exit(1)

# Initialize the OpenAI client
client = OpenAI(api_key=api_key)

# Store conversation history
conversation_history = []

print("Chatbot ready! Type 'quit' or 'exit' to end the conversation.\n")

while True:
    # Get user input
    user_input = input("You: ").strip()
    
    # Check if user wants to quit
    if user_input.lower() in ['quit', 'exit']:
        print("Goodbye!")
        break
    
    # Skip empty inputs
    if not user_input:
        continue
    
    # Add user message to conversation history
    conversation_history.append({"role": "user", "content": user_input})
    
    try:
        # Get response from OpenAI
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=conversation_history
        )
        
        # Extract assistant's reply
        assistant_message = response.choices[0].message.content
        
        # Add assistant's response to conversation history
        conversation_history.append({"role": "assistant", "content": assistant_message})
        
        # Display the response
        print(f"Bot: {assistant_message}\n")
        
    except Exception as e:
        print(f"Error: {e}\n")
        # Remove the last user message if there was an error
        conversation_history.pop()
