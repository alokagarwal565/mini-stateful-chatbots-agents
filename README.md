# OpenAI SDK Mini Projects

This repository contains two mini projects demonstrating how to use the OpenAI SDK with a custom `agents` library for building conversational AI agents in Python.

## Projects Overview

### 1. Basic Streaming Agent (`basic_agent.py`)

A straightforward implementation of a conversational agent that streams responses in real-time.

- **Features**:
  - Real-time response streaming.
  - Context-aware through `previous_response_id`.
  - Concise "helpful assistant" persona.
- **Workflow**: The user enters text, and the assistant streams back its response chunk by chunk.

### 2. History-Aware JSON Agent (`json_history_agent.py`)

An advanced agent implementation that persists conversation history to a local JSON file, allowing for session resumption.

- **Features**:
  - **Conversation Persistence**: All messages are saved to `conversation_history.json`.
  - **Session Management**: Users can enter a specific UUID or conversation ID to resume past chats.
  - **Rich Metadata**: Stores timestamps and roles (user/assistant) for every entry.
- **Workflow**: It loads existing history for the given ID, sends the full context to the model, and updates the local storage with new interactions.

---

## Setup Instructions

### Prerequisites

- Python 3.8+
- An OpenAI API Key

### Installation

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **Install dependencies**:

   ```bash
   pip install openai python-dotenv
   ```

   _(Note: Ensure you have access to the `agents` library used in the scripts)_

3. **Configure Environment**:
   Create a `.env` file in the root directory and add your OpenAI API key:
   ```env
   OPENAI_API_KEY=your_actual_api_key_here
   ```

---

## Usage

### Running the Basic Agent

```bash
python basic_agent.py
```

### Running the JSON History Agent

```bash
python json_history_agent.py
```

- When prompted, press **Enter** for a new session or provide a **UUID** to resume an existing one.

## Project Structure

- `basic_agent.py`: Simple streaming assistant implementation.
- `json_history_agent.py`: Assistant with persistent JSON history management.
- `conversation_history.json`: (Generated) Stores the chat history.
- `.env`: (Required) Environment variables for API authentication.
