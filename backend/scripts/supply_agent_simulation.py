from crewai import Agent, Crew, Task
from agents.supply_publisher_agent import publisher_agent
from agents.hospital_a_buyer_agent import buyer_agent_a
from agents.hospital_b_buyer_agent import buyer_agent_b
import os
import json
from dotenv import load_dotenv

# Load .env file from current directory
load_dotenv()

# Optional debug print
print("🔐 Loaded API Key:", os.getenv("OPENAI_API_KEY")[:8], "********")

# Shared negotiation transcript
chat_log = []

# Define agents
publisher_agent = Agent(
    role="Hospital Inventory Publisher",
    goal="Offer surplus medical inventory and finalize deals with buyers",
    backstory="You manage medical inventory and aim to efficiently reduce surplus through fair negotiation.",
    verbose=False
)

hospital_a_agent = Agent(
    role="Hospital A Buyer",
    goal="Negotiate to purchase required inventory at competitive pricing",
    backstory="You oversee procurement for Hospital A and aim to secure resources within a limited budget.",
    verbose=False
)

hospital_b_agent = Agent(
    role="Hospital B Buyer",
    goal="Negotiate deals for medical supplies within fiscal constraints",
    backstory="As a buyer for Hospital B, your objective is to fulfill supply needs cost-effectively.",
    verbose=False
)

# Define task-based rounds
tasks = [
    Task(description="Round 1: Publisher shares surplus inventory and opens the floor for negotiation.",
         expected_output="Initial message published to buyers.",
         agent=publisher_agent),
    Task(description="Round 2: Hospital A responds with a purchase offer.",
         expected_output="Hospital A proposes discounted rates.",
         agent=hospital_a_agent),
    Task(description="Round 3: Hospital B joins and presents its counter-offer.",
         expected_output="Hospital B expresses interest and shares terms.",
         agent=hospital_b_agent),
    Task(description="Round 4: Publisher evaluates both offers and makes a counter-proposal.",
         expected_output="Publisher suggests revised terms for anesthesia.",
         agent=publisher_agent),
    Task(description="Round 5: Hospital A responds to the revised pricing.",
         expected_output="Hospital A updates interest with a new counter.",
         agent=hospital_a_agent),
    Task(description="Round 6: Hospital B finalizes its request for partial quantity.",
         expected_output="Hospital B confirms quantity and pricing acceptance.",
         agent=hospital_b_agent),
    Task(description="Round 7: Publisher confirms allocation of inventory.",
         expected_output="Hospital A and B are informed of allocation outcome.",
         agent=publisher_agent),
    Task(description="Round 8: Publisher summarizes and closes the negotiation session.",
         expected_output="Formal closure with transaction summary.",
         agent=publisher_agent),
]

# Create crew with all agents
crew = Crew(
    agents=[publisher_agent, hospital_a_agent, hospital_b_agent],
    tasks=tasks,
    verbose=True
)
# Run the crew

# === Run negotiation ===
results = crew.kickoff()

# === Save messages in structured JSON format ===
chat_log = [{"round": 0, "role": "System", "content": "Negotiation Session Started"}]

for idx, task_output in enumerate(results.task_outputs):  # ✅ Use task_outputs
    if hasattr(task_output, "final_output") and task_output.final_output:
        chat_log.append({
            "round": idx + 1,
            "role": task_output.agent.role,
            "content": task_output.final_output.strip()
        })

chat_log.append({
    "round": len(chat_log),
    "role": "System",
    "content": "Session Closed"
})

# Save log
os.makedirs("data", exist_ok=True)
with open("data/chat_log.json", "w") as f:
    json.dump(chat_log, f, indent=2)

# === Reusable function for frontend trigger ===
def kickoff_negotiation():
    results = crew.kickoff()

    chat_log = [{"round": 0, "role": "System", "content": "Negotiation Session Started"}]

    for idx, task_output in enumerate(results.task_outputs):
        if hasattr(task_output, "final_output") and task_output.final_output:
            chat_log.append({
                "round": idx + 1,
                "role": task_output.agent.role,
                "content": task_output.final_output.strip()
            })

    chat_log.append({
        "round": len(chat_log),
        "role": "System",
        "content": "Session Closed"
    })

    os.makedirs("data", exist_ok=True)
    with open("data/chat_log.json", "w") as f:
        json.dump(chat_log, f, indent=2)

    return "Negotiation complete"