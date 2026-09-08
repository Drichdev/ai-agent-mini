# Local Text Agent

Conversational agent:

* **Input**: Text input
* **Reasoning**: A local GGUF LLM (`llama-cpp-python`) generates the response (`llm.py`, `agent.py`)
* **Memory**: SQLite stores user information across sessions (`db.py`)
* **Actions**: Web search (DuckDuckGo) and Wikipedia when needed (`tools.py`)

## Installation

```bash
pip install -r requirements.txt
```

## Running the Agent

```bash
python main.py
```

## Configuration

Everything can be configured using environment variables (see `config.py`). For example:

```bash
export LLM_REPO_ID=...           # Another GGUF model from Hugging Face
export DB_PATH=./agent_memory.sqlite3
```

## How the Model Calls a Tool

The model is relatively small (1.5B parameters). Instead of relying on native function calling, which can be unreliable at this model size, the agent uses a simple protocol defined in the system prompt (`config.py`).

When the model needs to use a tool, it responds with a single-line JSON object:

```json
{
  "tool": "web_search",
  "args": {
    "query": "weather in Lomé",
    "top_n": 3
  }
}
```

`agent.py` detects this format, executes the requested tool, and sends the result back to the model. The model then uses the tool output to generate its final response in natural language.

