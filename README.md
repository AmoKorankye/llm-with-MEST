# MEST Chat Logging Chatbot

A Python chatbot application that supports both OpenAI's GPT-4o-mini and local Ollama models, with comprehensive JSON-based logging for tracking conversations and performance metrics.

## Features

- **Dual Model Support**: Use OpenAI's GPT-4o-mini or run locally with Ollama's llama3.2:8b
- **Structured Logging**: All interactions logged to a JSON file with timestamps, session IDs, and performance metrics
- **Session Tracking**: Each chat session gets a unique session ID for easy log filtering
- **Performance Metrics**: Tracks response time and token usage for API calls
- **Error Handling**: Comprehensive error logging and graceful error messages

## Prerequisites

- Python 3.12+
- OpenAI API key (for OpenAI model)
- Ollama installed and running on localhost:11434 (for local model)

## Installation

1. **Create a virtual environment** (already set up in `mest/`):
   ```bash
   source mest/bin/activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   Create a `.env` file in the project root with your OpenAI API key:
   ```
   OPEN_AI_API_KEY=your_api_key_here
   ```

## Usage

Run the chatbot:
```bash
python mest_chat_logging.py
```

### Interactive Menu

1. When prompted, select your model:
   - **Option 1**: OpenAI GPT-4o-mini (requires valid API key)
   - **Option 2**: Ollama llama3.2:8b (requires Ollama running locally)

2. Start chatting by typing your messages
3. Type `exit` to end the conversation

### Example Session

```
Select Model Type
1. OpenAI GPT-4
2. Ollama (Local)
Enter chouce (1 or 2): 2

=== Chat Session Started ===
Using Ollama model
Type 'exit to end the conversations
Session ID: a96947be-4a56-48fe-965f-3bb11fe26b2c

You: What is the meaning of Life?
Bot: The meaning of life is a profound question that has been explored by philosophers, theologians, scientists, and thinkers throughout history.

You: exit
Goodbye!
```

## Logging

All conversations are automatically logged to `chatbot_logs.json` in a valid JSON array format. Each log entry contains:

### User Input Log
```json
{
  "timestamp": "2026-02-09T15:48:01.290461",
  "level": "INFO",
  "type": "user_input",
  "metadata": {
    "user_id": "a96947be-4a56-48fe-965f-3bb11fe26b2c",
    "session_id": "a96947be-4a56-48fe-965f-3bb11fe26b2c",
    "model": "llama3.2:8b"
  }
}
```

### Model Response Log
```json
{
  "timestamp": "2026-02-09T15:48:03.032504",
  "level": "INFO",
  "type": "model_response",
  "model_response": "Machine learning is...",
  "metadata": {
    "session_id": "a96947be-4a56-48fe-965f-3bb11fe26b2c",
    "model": "llama3.2:8b",
    "response_time_seconds": 1.741303,
    "tokens_used": 35
  }
}
```

### Error Log
```json
{
  "timestamp": "2026-02-09T15:48:05.100000",
  "level": "ERROR",
  "type": "error",
  "error_message": "Connection error",
  "metadata": {
    "session_id": "a96947be-4a56-48fe-965f-3bb11fe26b2c",
    "model": "llama3.2:8b",
    "user_id": "a96947be-4a56-48fe-965f-3bb11fe26b2c"
  }
}
```

## File Structure

```
.
├── mest_chat_logging.py      # Main chatbot application
├── chatbot_logs.json         # JSON log file (auto-created)
├── requirements.txt          # Python dependencies
├── .env                       # Environment variables (not in repo)
└── README.md                 # This file
```

## Configuration

### Models Available

- **OpenAI**: `gpt-4o-mini` (requires API key and internet connection)
- **Ollama**: `llama3.2:8b` (runs locally, no API key needed)

### System Prompt

The default system prompt is:
> "You are a helpful assistant that can answer questions and help with tasks."

To modify this, edit line 70 in `mest_chat_logging.py`.

## Troubleshooting

### API Key Issues
- Ensure `.env` file contains `OPEN_AI_API_KEY=your_key_here`
- Verify the API key is valid on OpenAI's website

### Ollama Connection Issues
- Ensure Ollama is running: `ollama serve`
- Verify Ollama is accessible at `http://localhost:11434`
- Ensure `llama3.2:8b` is downloaded: `ollama pull llama3.2:8b`

### JSON Log File Corruption
- Delete `chatbot_logs.json` and restart the application
- It will be automatically recreated as a valid JSON array

### Import Errors
- Make sure virtual environment is activated: `source mest/bin/activate`
- Reinstall dependencies: `pip install -r requirements.txt`

## Dependencies

- `openai>=2.0` - OpenAI API client
- `python-dotenv` - Environment variable management
- `tqdm` - Progress bar utility
- `httpx` - HTTP client library
- `pydantic` - Data validation

See `requirements.txt` for full dependency list.
