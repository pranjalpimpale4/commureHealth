from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
import random
from dotenv import load_dotenv
load_dotenv()

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)

# Define a simple quote agent
quote_agent = Agent(
    role="motivational thinker",
    goal="inspire users with brief and uplifting quotes",
    backstory="You are an AI that delivers motivational wisdom in one line.",
    verbose=False,
    allow_delegation=False,
    llm=llm
)

# Example tasks the agent could perform
def get_random_quote():
    topics = ["perseverance", "growth", "learning", "resilience", "vision"]
    topic = random.choice(topics)
    task = Task(
        description=f"Give a short, inspiring quote about {topic}. One sentence only.",
        expected_output="A one-sentence motivational quote.",
        agent=quote_agent
    )

    crew = Crew(
        agents=[quote_agent],
        tasks=[task],
        verbose=False
    )
    return crew.kickoff()
