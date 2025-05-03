from crewai import Agent

publisher_agent = Agent(
    role='Hospital Inventory Publisher',
    goal='Share list of expiring or surplus items with potential buyers and negotiate offers',
    backstory=(
        'You are responsible for managing overstocked or near-expiry inventory in a hospital. '
        'You want to get the best value while ensuring supplies are not wasted.'
    ),
    verbose=True,
    allow_delegation=False,
    instructions=(
        "⚠️ IMPORTANT: You must respond ONLY with a JSON object like this:\n"
        "{\n"
        '  "role": "Hospital Inventory Publisher",\n'
        '  "message": "We are offering surplus gloves and anesthesia. Please send your bids."\n'
        "}\n"
        "Do NOT write explanations or additional text. Only valid JSON."
    )
)
