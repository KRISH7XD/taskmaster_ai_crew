from crewai import Crew, Task
from agents import planner_agent, research_agent, execution_agent, coordinator_agent
from feedback import feedback
import uuid


user_request = "Generate a one-sentence summary of AI agents and save it to a file."
task_id = str(uuid.uuid4())


planning_task = Task(
    description=f"Break down this request into steps: {user_request}",
    agent=planner_agent,
    expected_output="A list of steps to complete the request."
)

research_task = Task(
    description="Research AI agents and provide key information.",
    agent=research_agent,
    expected_output="A short paragraph or key points about AI agents."
)

execution_task = Task(
    description="Generate a one-sentence summary based on research and save it to 'summary.txt'.",
    agent=execution_agent,
    expected_output="Confirmation that the summary was written to a file."
)

coordination_task = Task(
    description="Review the plan, research, and execution; adjust if needed.",
    agent=coordinator_agent,
    expected_output="Final approval or corrections."
)


crew = Crew(
    agents=[planner_agent, research_agent, execution_agent, coordinator_agent],
    tasks=[planning_task, research_task, execution_task, coordination_task],
    verbose=2  
)


feedback.start_task(task_id)
result = crew.kickoff()
duration = feedback.end_task(task_id, success=True)


print("Final Result:", result)
print(f"Task completed in {duration:.2f} seconds")