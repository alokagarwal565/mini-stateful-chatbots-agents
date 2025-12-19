import asyncio
import os
import json
import uuid
from datetime import datetime
from agents import Agent, Runner
from dotenv import load_dotenv
from openai.types.responses import ResponseTextDeltaEvent

load_dotenv()
    
HISTORY_FILE = os.path.join(os.path.dirname(__file__), "conversation_history.json")

def save_entry(conversation_id, role, content):

    entry = {
        "timestamp": datetime.now().isoformat(),
        "role": role,
        "content": content
    }
    
    history_data = {}
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                history_data = json.load(f)
                if not isinstance(history_data, dict):
                    if isinstance(history_data, list):
                        history_data = {"legacy": history_data}
                    else:
                        history_data = {}
        except (json.JSONDecodeError, IOError):
            history_data = {}
            
    if conversation_id not in history_data:
        history_data[conversation_id] = []
        
    history_data[conversation_id].append(entry)
    
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history_data, f, indent=2, ensure_ascii=False)
    except IOError as e:
        print(f"Error saving history: {e}")

async def main():
    agent = Agent(
        name="HistoryAwareAssistant",
        instructions="You are a helpful assistant. Be VERY concise.",
    )

    print("Chat with the assistant! Type 'exit' or 'quit' to stop.")
    print(f"Conversation history will be saved to: {HISTORY_FILE}")
    
    conversation_id = input("Enter conversation ID to resume (or press Enter for new): ").strip()
    if not conversation_id:
        conversation_id = str(uuid.uuid4())
    print(f"Using Conversation ID: {conversation_id}")
    
    while True:
        try:
            user_input = input("You: ").strip()
            if user_input.lower() in ["exit", "quit"]:
                print("Goodbye!")
                break
            
            if not user_input:
                continue
            
            save_entry(conversation_id, "user", user_input)
            
            conversation_history = []
            if os.path.exists(HISTORY_FILE):
                try:
                    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                        file_data = json.load(f)
                        if isinstance(file_data, dict) and conversation_id in file_data:
                            raw_history = file_data[conversation_id]
                            conversation_history = [
                                {"role": entry["role"], "content": entry["content"]} 
                                for entry in raw_history 
                                if "role" in entry and "content" in entry
                            ]
                except Exception:
                    conversation_history = []

            print("Assistant: ", end="", flush=True)
            result = Runner.run_streamed(
                agent, 
                conversation_history
            )
            
            full_response = ""
            async for event in result.stream_events():
                if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                    chunk = event.data.delta
                    print(chunk, end="", flush=True)
                    full_response += chunk
            
            print()
            save_entry(conversation_id, "assistant", full_response)
                        
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())