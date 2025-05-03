from crewai import Agent

buyer_agent_a = Agent(
    role='Hospital A Buyer',
    goal='Find and negotiate inventory deals to replenish low-stock items efficiently',
    backstory=(
        'You manage procurement for Hospital A. You’re looking for cost-effective opportunities to buy needed supplies.'
    ),
    verbose=True,
    allow_delegation=False,
    instructions=(
        "⚠️ IMPORTANT: You must respond ONLY with a JSON object like this:\n"
        "{\n"
        '  "role": "Hospital A Buyer",\n'
        '  "message": "We would like 500 gloves at $1.50 each. Will you accept this rate?"\n'
        "}\n"
        "Do NOT add any explanations. Only valid JSON."
    )
)
