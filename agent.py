# agent.py

from langchain_mistralai import ChatMistralAI
from langchain.agents import Tool, AgentExecutor, create_tool_calling_agent
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

import os
import time
from dotenv import load_dotenv

load_dotenv()

# Step 1: Initialize Mistral LLM
llm = ChatMistralAI(
    model="mistral-large-latest",
    mistral_api_key=os.getenv("MISTRAL_API_KEY"),
    temperature=0.7,
    model_kwargs={"max_tokens": 500}
)

# Step 2: Define Game State
class GameState:
    def __init__(self):
        self.location = "dungeon_entrance"
        self.inventory = []
        self.monsters = {
            "dungeon_entrance": ["Thunderbeak Wyvern"],
            "hallway": ["Shadowy Skeleton"]
        }

    def move_to(self, location):
        if location in self.monsters:
            self.location = location
            return f"You moved to {location}."
        return f"You can't go to {location}."

    def get_monsters_in_current_location(self):
        return self.monsters.get(self.location, [])

game_state = GameState()

# Step 3: Define Tools
def move_tool(location: str) -> str:
    return game_state.move_to(location)

def list_monsters_tool(_) -> str:
    monsters = game_state.get_monsters_in_current_location()
    if monsters:
        return "Monsters here: " + ", ".join(monsters)
    return "No monsters here."

tools = [
    Tool(
        name="MoveToLocation",
        func=move_tool,
        description="Move the player to a new location in the game world."
    ),
    Tool(
        name="ListMonsters",
        func=list_monsters_tool,
        description="List all monsters in the current location."
    )
]

# Step 4: Create Prompt with Tool Calling Support
system_prompt = """
You are the Dungeon Master AI. Your role is to:
1. Use the 'MoveToLocation' tool when the player wants to explore.
2. Use the 'ListMonsters' tool to show enemies in the current area.
3. Describe the world dynamically based on the player's actions.

TOOLS:
-----
{tools}

Begin!
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad")
])

# Step 5: Create Agent with Tool Calling Support
agent = create_tool_calling_agent(llm, tools, prompt)

# Step 6: Initialize Memory
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Step 7: Create AgentExecutor with Memory
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, memory=memory)

# Step 8: Run Agent
def run_agent(query):
    time.sleep(2)  # Rate limit mitigation
    response = agent_executor.invoke({
        "input": query,
        "tools": tools
    })
    return response["output"]