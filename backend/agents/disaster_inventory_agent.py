# import os
# import json
# from crewai import Agent, Task, Crew
# from dotenv import load_dotenv
# from langchain_openai import ChatOpenAI

# from db import get_session
# from tools.fetch_disasters import DisasterFetcher
# from tools.check_proximity import ProximityChecker
# from tools.inventory_assessor import InventoryAssessor

# # Load OpenAI key from .env or environment
# load_dotenv()
# os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# llm = ChatOpenAI(model="gpt-4", temperature=0.3)

# # === AGENTS ===
# fetch_agent = Agent(
#     role="Disaster Intelligence Agent",
#     goal="Identify recent disasters near the hospital",
#     backstory="You scan global emergency feeds and filter out only disasters that are geographically close to the hospital.",
#     allow_delegation=False,
#     verbose=True,
#     llm=llm
# )

# inventory_agent = Agent(
#     role="Inventory Analyst Agent",
#     goal="Analyze hospital inventory for understocked items",
#     backstory="You check the hospital inventory and flag items that are below safe threshold levels.",
#     allow_delegation=False,
#     verbose=True,
#     llm=llm
# )

# strategy_agent = Agent(
#     role="Logistics Strategist Agent",
#     goal="Recommend restocking actions based on emergency risks and current inventory",
#     backstory="You synthesize emergency risk data and current inventory gaps to decide which supplies the hospital should urgently restock.",
#     allow_delegation=False,
#     verbose=True,
#     llm=llm
# )

# # === RUN TOOLS FIRST (before kicking off Crew) ===
# print("🔍 Running disaster and inventory tools...")
# raw_disasters = DisasterFetcher().get_disasters()
# nearby_disasters = ProximityChecker().filter_nearby_events(raw_disasters)

# with get_session() as session:
#     full_inventory = InventoryAssessor(session).get_inventory()
#     # Prepare summaries for LLM agents
#     disaster_summary = json.dumps(nearby_disasters, indent=2)
#     inventory_json = json.dumps([item.dict() for item in full_inventory], indent=2)

#     # === TASKS ===
#     fetch_task = Task(
#         description=(
#             "You already have a summary of recent disasters near the hospital (within 500km).\n"
#             "Review and briefly describe them for other agents.\n"
#             f"\nDisasters:\n{disaster_summary}"
#         ),
#         expected_output="Summary of relevant disaster situations.",
#         agent=fetch_agent
#     )

#     inventory_task = Task(
#         description=(
#             "You are provided with full hospital inventory data retrieved from the database.\n"
#             "Analyze and identify items that are understocked or critical.\n"
#             f"\nInventory:\n{inventory_json}"
#         ),
#         expected_output="Summary of understocked critical supplies.",
#         agent=inventory_agent
#     )

#     strategy_task = Task(
#         description=(
#             "You are given disaster context and complete hospital inventory data.\n"
#             "Recommend which items should be restocked urgently.\n"
#             "Include item_id and a recommended 'needed' count with 10% safety margin.\n"
#             f"\nDisasters:\n{disaster_summary}\n\nInventory:\n{inventory_json}"
#         ),
#         expected_output="JSON list like: [{\"item_id\": 2, \"needed\": 60}, ...]",
#         agent=strategy_agent
#     )

#     # === CREW ===
#     crew = Crew(
#         agents=[fetch_agent, inventory_agent, strategy_agent],
#         tasks=[fetch_task, inventory_task, strategy_task],
#         verbose=True
#     )

#     if __name__ == "__main__":
#         print("🚨 Starting Multi-Agent Disaster Inventory Crew...")
#         final_output = crew.kickoff()
#         print("✅ Final Recommendation Output:")
#         print(final_output)

#         # Ensure it's JSON serializable
#         output_result = final_output.result if hasattr(final_output, "result") else str(final_output)

#         # Save to JSON
#         output_path = os.path.join("data", "needed_supplies.json")
#         os.makedirs(os.path.dirname(output_path), exist_ok=True)
#         with open(output_path, "w") as f:
#             json.dump({"recommendations": output_result}, f, indent=2)
#         print(f"📁 Output saved to: {output_path}")


import os
import json
from crewai import Agent, Task, Crew
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from db import get_session
from tools.fetch_disasters import DisasterFetcher
from tools.check_proximity import ProximityChecker
from tools.inventory_assessor import InventoryAssessor

# Load OpenAI key
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(model="gpt-4", temperature=0.3)

# === AGENTS ===
fetch_agent = Agent(
    role="Disaster Intelligence Agent",
    goal="Identify recent disasters near the hospital",
    backstory="You scan global emergency feeds and filter out only disasters that are geographically close to the hospital.",
    allow_delegation=False,
    verbose=True,
    llm=llm
)

inventory_agent = Agent(
    role="Inventory Analyst Agent",
    goal="Analyze hospital inventory for understocked items",
    backstory="You check the hospital inventory and flag items that are below safe threshold levels.",
    allow_delegation=False,
    verbose=True,
    llm=llm
)

strategy_agent = Agent(
    role="Logistics Strategist Agent",
    goal="Recommend restocking actions based on emergency risks and current inventory",
    backstory="You synthesize emergency risk data and current inventory gaps to decide which supplies the hospital should urgently restock.",
    allow_delegation=False,
    verbose=True,
    llm=llm
)

def run_disaster_inventory_agent() -> list[dict]:
    print("🚨 Starting Multi-Agent Disaster Inventory Crew...")

    # Step 1: Fetch and filter disasters
    raw_disasters = DisasterFetcher().get_disasters()
    nearby_disasters = ProximityChecker().filter_nearby_events(raw_disasters)

    with get_session() as session:
        # Step 2: Load inventory
        full_inventory = InventoryAssessor(session).get_inventory()

        # Step 3: Format data for LLM input
        disaster_summary = json.dumps(nearby_disasters, indent=2)
        inventory_json = json.dumps([item.dict() for item in full_inventory], indent=2)

        # Step 4: Define tasks for CrewAI agents
        fetch_task = Task(
            description=(
                "You already have a summary of recent disasters near the hospital (within 500km).\n"
                "Review and briefly describe them for other agents.\n"
                f"\nDisasters:\n{disaster_summary}"
            ),
            expected_output="Summary of relevant disaster situations.",
            agent=fetch_agent
        )

        inventory_task = Task(
            description=(
                "You are provided with full hospital inventory data retrieved from the database.\n"
                "Analyze and identify items that are understocked or critical.\n"
                f"\nInventory:\n{inventory_json}"
            ),
            expected_output="Summary of understocked critical supplies.",
            agent=inventory_agent
        )

        strategy_task = Task(
            description=(
                "You are given disaster context and complete hospital inventory data.\n"
                "Recommend which items should be restocked urgently.\n"
                "Include item_id and a recommended 'needed' count with 10% safety margin.\n"
                f"\nDisasters:\n{disaster_summary}\n\nInventory:\n{inventory_json}"
            ),
            expected_output="JSON list like: [{\"item_id\": 2, \"needed\": 60}, ...]",
            agent=strategy_agent
        )

        # Step 5: Execute Crew
        crew = Crew(
            agents=[fetch_agent, inventory_agent, strategy_agent],
            tasks=[fetch_task, inventory_task, strategy_task],
            verbose=True
        )

        result = crew.kickoff()
        print("✅ Final Recommendation Output:")
        print(result)

        # Step 6: Parse Crew result
        output = result.result if hasattr(result, "result") else str(result)

        try:
            parsed = json.loads(output)

            if isinstance(parsed, list):
                return parsed
        except Exception as e:
            print(f"⚠️ Failed to parse result as JSON: {e}")

        return []
