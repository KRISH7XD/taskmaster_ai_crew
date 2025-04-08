import streamlit as st
from crewai import Crew, Task
from agents import planner_agent, research_agent, execution_agent, coordinator_agent
from feedback import feedback
import uuid
import os
import time


st.set_page_config(page_title="TaskMaster AI Crew", layout="wide")


st.title("TaskMaster AI Crew")
st.subheader("A Multi-Agent System Powered by Llama 4 Maverick")
st.write("Enter a task below, and watch our AI agents collaborate to complete it!")


with st.sidebar:
    st.header("Settings")
    st.info("Using OpenRouter's Llama 4 Maverick API for advanced reasoning.")
    st.write("**Agents:** Planner, Researcher, Executor, Coordinator")
    st.write("**Tools:** Web Search, File Writing, Code Execution, GitHub API, Local Code Runner, Resume Builder, File Reader")


st.header("Task Input")
user_request = st.text_area("Enter your task here:", 
                            placeholder="e.g., Add ‘Developed a multi-agent AI system using CrewAI’ to my resume and save it to ‘resume.txt’.",
                            height=100)


if st.button("Run Task", key="run_button"):
    if not user_request:
        st.error("Please enter a task!")
    else:
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        
        task_id = str(uuid.uuid4())

        
        planning_task = Task(
            description=f"Break down this request into steps: {user_request}",
            agent=planner_agent,
            expected_output="A list of steps to complete the request."
        )
        research_task = Task(
            description="Research the topic and provide key information.",
            agent=research_agent,
            expected_output="A short paragraph or key points."
        )
        execution_task = Task(
            description=f"Execute the task based on research and save results: {user_request}",
            agent=execution_agent,
            expected_output="Confirmation of task completion."
        )
        coordination_task = Task(
            description="Review the plan, research, and execution; adjust if needed.",
            agent=coordinator_agent,
            expected_output="Final approval or corrections."
        )

        
        crew = Crew(
            agents=[planner_agent, research_agent, execution_agent, coordinator_agent],
            tasks=[planning_task, research_task, execution_task, coordination_task],
            verbose=True
        )

        #
        feedback.start_task(task_id)
        status_text.text("Planning...")
        progress_bar.progress(25)
        time.sleep(0.5)
        
        status_text.text("Researching...")
        progress_bar.progress(50)
        time.sleep(0.5)
        
        status_text.text("Executing...")
        progress_bar.progress(75)
        time.sleep(0.5)
        
        result = crew.kickoff()
        duration = feedback.end_task(task_id, success=True)
        
        status_text.text("Coordinating...")
        progress_bar.progress(100)
        time.sleep(0.5)
        status_text.text("Task Completed!")

        
        st.header("Results", divider="gray")
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Planner Output")
            st.code(planning_task.output.raw if planning_task.output else "No output generated.")
        
        with col2:
            st.subheader("Researcher Output")
            st.code(research_task.output.raw if research_task.output else "No output generated.")
        
        col3, col4 = st.columns(2)
        
        with col3:
            st.subheader("Executor Output")
            st.code(execution_task.output.raw if execution_task.output else "No output generated.")
        
        with col4:
            st.subheader("Coordinator Output")
            st.code(coordination_task.output.raw if coordination_task.output else "No output generated.")

        
        st.subheader("Final Result", divider="gray")
        st.success(result)

        
        output_dir = "output"
        if os.path.exists(output_dir):
            files = [f for f in os.listdir(output_dir) if os.path.isfile(os.path.join(output_dir, f))]
            if files:
                for file in files:
                    with open(os.path.join(output_dir, file), "r") as f:
                        st.download_button(
                            label=f"Download {file}",
                            data=f,
                            file_name=file,
                            mime="text/plain",
                            key=f"download_{file}"
                        )
            else:
                st.warning("No files generated in 'output/' directory.")
        else:
            st.warning("Output directory not found.")

        
        st.subheader("Performance Metrics", divider="gray")
        st.metric("Task Completion Time", f"{duration:.2f} seconds")


st.markdown("---")
st.write("Built with Streamlit, CrewAI, and OpenRouter's Llama 4 Maverick API.")