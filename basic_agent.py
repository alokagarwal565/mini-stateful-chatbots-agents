import asyncio
import os
from agents import Agent, Runner
from dotenv import load_dotenv
from openai.types.responses import ResponseTextDeltaEvent

load_dotenv()

async def main():
    agent = Agent(
        name="Assistant",
        instructions="You are a helpful assistant. Be VERY concise.",
    )

    print("Chat with the assistant! Type 'exit' or 'quit' to stop.")
    previous_response_id = None

    while True:
        try:
            user_input = input("You: ").strip()
            if user_input.lower() in ["exit", "quit"]:
                print("Goodbye!")
                break
            
            if not user_input:
                continue
            
            print("Assistant: ", end="", flush=True)
            result = Runner.run_streamed(
                agent, 
                user_input, 
                previous_response_id=previous_response_id
            )
            
            async for event in result.stream_events():
                if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                    print(event.data.delta, end="", flush=True)
            
            print()
            previous_response_id = result.last_response_id
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())
