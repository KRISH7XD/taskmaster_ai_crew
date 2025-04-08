import os
from dotenv import load_dotenv
from crewai import Agent
from litellm import completion
from config import OPENROUTER_API_KEY, MODEL_NAME
from tools import tools_list, tavily_search_tool
from memory import add_to_memory, retrieve_from_memory


class OpenRouterLLM:
    def __init__(self):
        self.api_key = OPENROUTER_API_KEY
        self.model = f"openrouter/{MODEL_NAME}"
        self.max_tokens = 500
        self.temperature = 0.7

    def call(self, messages, **kwargs):
        response = completion(
            model=self.model,
            messages=messages,
            api_key=self.api_key,
            base_url="https://openrouter.ai/api/v1",
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            headers={"Authorization": f"Bearer {self.api_key}"}
        )
        return response.choices[0].message.content

llm = OpenRouterLLM()

# Planner Agent
planner_agent = Agent(
    role="Planner",
    goal="Break down user requests into actionable steps",
    backstory="A strategic mastermind who creates efficient plans.",
    llm=llm,
    tools=[],
    verbose=True,
    memory=(add_to_memory, retrieve_from_memory)
)

# Research Agent
research_agent = Agent(
    role="Researcher",
    goal="Gather relevant information to support task execution",
    backstory="A curious investigator skilled at finding insights.",
    llm=llm,
    tools=[tavily_search_tool],
    verbose=True,
    memory=(add_to_memory, retrieve_from_memory)
)

execution_agent = Agent(
    role="Executor",
    goal="Perform tasks using tools and save results",
    backstory="A reliable doer who gets things done with precision.",
    llm=llm,
    tools=tools_list,  # Includes read_file
    verbose=True,
    memory=(add_to_memory, retrieve_from_memory)
)

# Coordinator Agent
coordinator_agent = Agent(
    role="Coordinator",
    goal="Oversee progress and ensure tasks align with the plan",
    backstory="A vigilant overseer who keeps the team on track.",
    llm=llm,
    tools=[],
    verbose=True,
    memory=(add_to_memory, retrieve_from_memory)
)