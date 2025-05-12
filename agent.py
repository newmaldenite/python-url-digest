# agent.py

from langchain.agents import Tool, AgentExecutor, create_tool_calling_agent
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import PromptTemplate, MessagesPlaceholder
from langchain.prompts import MessagesPlaceholder
from langchain_mistralai import ChatMistralAI

import os
from dotenv import load_dotenv

load_dotenv()

# Step 1: Initialize Mistral LLM
llm = ChatMistralAI(
    model="mistral-small-latest",
    mistral_api_key=os.getenv("MISTRAL_API_KEY"),
    temperature=0.7
)

# ----------------------
# Custom Tool: Narrative Generator
# ----------------------
def generate_narrative(input_text):
    """
    This function is called by the agent to generate story content,
    descriptions, encounters, or resolve actions based on player input.
    """
    # Define the prompt for the LLM
    prompt = f"""
You are The ForestMaster, a fun and engaging Dungeon Master guiding a player through a mystical forest adventure.

Your current objective is: To lead a single player through a dynamic, narrative-driven journey in a mysterious forest, encouraging exploration, decision-making, and character development.

Traits:
- Imaginative
- Responsive
- Descriptive
- Adaptive to player choices
- Encouraging of creative solutions

Constraints:
- The player begins in a clearing in the center of the forest.
- The player can move in any direction (north, south, east, west, or explore points of interest).
- Each location should present atmosphere, potential encounters, and narrative intrigue.
- Trials must focus on testing the player’s connection with nature—this could involve empathy, intuition, survival instincts, or moral dilemmas.
- Encounters may include friendly or hostile characters/creatures typical of fantasy RPGs (e.g., elves, goblins, spirits, talking animals, druids).
- All combat must be resolvable via dialogue and strategy—describe opponents' behaviors or fighting styles clearly so players can exploit weaknesses.
- Use vivid but concise fantasy-style descriptions; keep tone light and engaging.

Player Input: {input_text}

Respond in character as ForestMaster. Describe what happens next in the game world.
"""
    response = llm.invoke(prompt)
    return response.content

# Wrap the function into a Tool
narrative_tool = Tool(
    name="NarrativeGenerator",
    func=generate_narrative,
    description="Generates immersive narrative responses as the Dungeon Master based on player input."
)

# ----------------------
# Initialize Agent
# ----------------------


tools = [narrative_tool]

# Define system prompt
system_prompt = """
You are ForestMaster, a Dungeon Master guiding a player through a fantasy forest adventure.

Use the NarrativeGenerator tool to describe locations, encounters, and outcomes.
Maintain a light and vivid storytelling style.

Do NOT mention any internal processes or tools directly to the player.

Chat History: {chat_history}
Agent Scratchpad: {agent_scratchpad}
Player Input: {input}
"""

# Wrap it in a PromptTemplate
prompt = PromptTemplate.from_template(system_prompt).partial(
    chat_history=MessagesPlaceholder(variable_name="chat_history")
)

# Set up memory
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Create agent
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=False, memory=memory)

# ----------------------
# Start the Adventure!
# ----------------------

print("🌲 Welcome to the Mysterious Forest!\n")
print("You find yourself standing in a quiet clearing surrounded by ancient trees. Sunlight filters through the canopy above.\n")
print("Which direction would you like to go? North, South, East, West... or explore something nearby?\n")

while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        print("🌲 Thanks for playing!")
        break
    response = agent_executor.invoke({"input": user_input})
    print(f"ForestMaster: {response['output']}\n")