#!/usr/bin/env python3
# agents/recurrence_agent.py

import os
import json
from dotenv import load_dotenv
from crewai import Agent, Task, Crew

def parse_agent_output(raw_text):
    """Attempt to JSON-decode an agent's raw_output string."""
    try:
        return json.loads(raw_text.strip())
    except Exception as e:
        print(f"⚠️ Could not parse agent output:\n{raw_text}\nError: {e}")
        return []

def main():
    # load API key
    load_dotenv()
    if "OPENAI_API_KEY" not in os.environ:
        print("❌ Please set OPENAI_API_KEY in your .env")
        return

    # 1) Read your Prophet forecast
    with open("data/activity_forecast_llm_ready.json") as f:
        forecast_data = json.load(f)["forecast"]

    # 2) Build the two agents + tasks exactly as you did
    hospital_location = "San Francisco, California"

    dem_agent = Agent(
        role="Demographic Evaluator",
        goal="Compute demographic-driven adjustment coefficients",
        backstory=(
            f"You are a healthcare forecasting expert in {hospital_location}. "
            "You know how age, gender split, and 2-year growth patterns affect volumes."
        ),
        verbose=False
    )
    dem_task = Task(
        description=(
            f"Forecast data:\n{json.dumps(forecast_data,indent=2)}\n\n"
            "Based solely on demographics, return a JSON array like:\n"
            "[ {\"activity_type\":\"Ortho_appointment\",\"demographic_coefficient\":1.15}, … ]\n"
            "— raw JSON only."
        ),
        expected_output="JSON list of {activity_type, demographic_coefficient}",
        agent=dem_agent
    )

    reg_agent = Agent(
        role="Regional Evaluator",
        goal="Compute region/season-driven adjustment coefficients",
        backstory=(
            f"You are a healthcare forecasting expert in {hospital_location}. "
            "You know how seasonality, climate, and local public health trends modify demand."
        ),
        verbose=False
    )
    reg_task = Task(
        description=(
            f"Forecast data:\n{json.dumps(forecast_data,indent=2)}\n\n"
            "Based solely on regional factors, return a JSON array like:\n"
            "[ {\"activity_type\":\"Ortho_appointment\",\"regional_coefficient\":1.25}, … ]\n"
            "— raw JSON only."
        ),
        expected_output="JSON list of {activity_type, regional_coefficient}",
        agent=reg_agent
    )

    # 3) Kick off the crew
    crew = Crew(agents=[dem_agent, reg_agent], tasks=[dem_task, reg_task], verbose=False)
    raw_results = crew.kickoff()

    # 4) Force into a list so indexing works
    outputs = raw_results if isinstance(raw_results, list) else [raw_results]

    if len(outputs) != 2:
        print(f"❌ Expected 2 outputs but got {len(outputs)}")
        return

    # 5) Extract each agent’s raw_output
    dem_raw = getattr(outputs[0], "raw_output", "")
    reg_raw = getattr(outputs[1], "raw_output", "")

    # 6) Parse them into Python lists
    dem_list    = parse_agent_output(dem_raw)
    region_list = parse_agent_output(reg_raw)

    # 7) Build lookup maps
    dem_map = { d["activity_type"]: d["demographic_coefficient"] for d in dem_list    }
    reg_map = { r["activity_type"]: r["regional_coefficient"]    for r in region_list }

    # 8) Merge into your final output
    final_output = []
    for entry in forecast_data:
        atype = entry["activity_type"]
        final_output.append({
            "activity_type":           atype,
            "demographic_coefficient": dem_map.get(atype, 1.0),
            "regional_coefficient":    reg_map.get(atype, 1.0),
        })

    # 9) Write it out
    os.makedirs("data", exist_ok=True)
    out_path = "data/forecast_coefficients_sanfrancisco.json"
    with open(out_path, "w") as f:
        json.dump(final_output, f, indent=2)

    print(f"✅ Saved merged coefficients to {out_path}")

if __name__ == "__main__":
    main()


# # 🔧 Install dependencies
# # !pip install -q crewai openai

# # # 📤 Upload your forecast file
# # from google.colab import files
# # uploaded = files.upload()  # Upload 'activity_forecast_llm_ready.json'

# # 🔑 Hard-coded OpenAI API key
# import os, json
# os.environ["OPENAI_API_KEY"] = "sk-proj-2FFy3HfeKeK-2gByWcDKL4utxotZ2v8s7jJIWSlTLPq2r3izHmh84..."

# # 📦 Imports
# from crewai import Agent, Task, Crew

# # 🏥 Hospital location context
# hospital_location = "San Francisco, California"

# # 📈 Load your Prophet forecast
# with open("data/activity_forecast_llm_ready.json") as f:
#     forecast_data = json.load(f)["forecast"]

# # 🤖 Agent 1: Demographic Evaluator
# dem_agent = Agent(
#     role="Demographic Evaluator",
#     goal="Compute demographic-driven adjustment coefficients for multiple forecast entries",
#     backstory=(
#         f"You are a healthcare forecasting expert evaluating appointment and surgery "
#         f"volumes for a hospital in {hospital_location}. You know how age cohorts, gender "
#         "ratios, and recent historical growth impact different activity types."
#     ),
#     verbose=True
# )
# dem_task = Task(
#     description=(
#         f"Here is the forecast data:\n{json.dumps(forecast_data, indent=2)}\n\n"
#         "Based solely on demographics (age distribution, gender split, historical two-year "
#         "growth patterns), return a JSON list of objects like:\n"
#         "[\n"
#         "  {\"activity_type\":\"Ortho_appointment\",\"demographic_coefficient\":1.15},\n"
#         "  ...\n"
#         "]\n\n"
#         "— No extra text or markdown, only the raw JSON array."
#     ),
#     expected_output="JSON list of {activity_type, demographic_coefficient}",
#     agent=dem_agent
# )

# # 🤖 Agent 2: Regional Evaluator
# reg_agent = Agent(
#     role="Regional Evaluator",
#     goal="Compute region/season-driven adjustment coefficients for multiple forecast entries",
#     backstory=(
#         f"You are a healthcare forecasting expert evaluating how location, climate, seasonality "
#         f"and local health trends in {hospital_location} modify forecasted demand volumes."
#     ),
#     verbose=True
# )
# reg_task = Task(
#     description=(
#         f"Here is the forecast data:\n{json.dumps(forecast_data, indent=2)}\n\n"
#         "Based solely on regional factors (seasonality, local environment, public health trends), "
#         "return a JSON list of objects like:\n"
#         "[\n"
#         "  {\"activity_type\":\"Ortho_appointment\",\"regional_coefficient\":1.25},\n"
#         "  ...\n"
#         "]\n\n"
#         "— No extra text or markdown, only the raw JSON array."
#     ),
#     expected_output="JSON list of {activity_type, regional_coefficient}",
#     agent=reg_agent
# )

# # 🚀 Run both agents together
# crew_agents = [dem_agent, reg_agent]
# crew_tasks  = [dem_task, reg_task]
# crew = Crew(agents=crew_agents, tasks=crew_tasks, verbose=True)
# results = crew.kickoff()

# # 🔄 Parse each agent’s raw_output
# def parse_agent_output(raw_text):
#     try:
#         return json.loads(raw_text.strip())
#     except Exception as e:
#         print(f"⚠️ Could not parse raw_output:\n{raw_text}\nError: {e}")
#         return []

# dem_list    = []
# region_list = []

# for agent_obj, result in zip(crew_agents, results if isinstance(results, list) else [results]):
#     raw = getattr(result, "raw_output", None)
#     if not isinstance(raw, str):
#         print(f"⚠️ No raw_output string found in result:\n{result}")
#         continue

#     parsed = parse_agent_output(raw)
#     if agent_obj.role.startswith("Demographic"):
#         dem_list = parsed
#     else:
#         region_list = parsed

# # 🔗 Merge into final structure
# dem_map = { d["activity_type"]: d["demographic_coefficient"] for d in dem_list }
# reg_map = { r["activity_type"]: r["regional_coefficient"]    for r in region_list }

# final_output = []
# for entry in forecast_data:
#     atype = entry["activity_type"]
#     final_output.append({
#         "activity_type":              atype,
#         "demographic_coefficient":    dem_map.get(atype, 1.0),
#         "regional_coefficient":       reg_map.get(atype, 1.0),
#     })

# # 💾 Save & download
# output_file = "forecast_coefficients_sanfrancisco.json"
# with open(output_file, "w") as f:
#     json.dump(final_output, f, indent=2)

# print(f"✅ Saved to {output_file}, now downloading...")
# from google.colab import files as fc
# fc.download(output_file)
