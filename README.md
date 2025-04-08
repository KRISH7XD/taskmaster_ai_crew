TaskMaster AI Crew
A multi-agent AI system built using CrewAI, LiteLLM, and Streamlit to automate complex tasks such as planning, research, code execution, and resume generation. Powered by LLMs like LLaMA 4 Maverick via OpenRouter, this project showcases a collaborative framework between specialized agents for efficient task completion.

Features
Multi-Agent System: Four CrewAI agents—Planner, Researcher, Executor, and Coordinator—working in a sequential pipeline.

Code Execution Tool: Execute Python, C, C++, and Java code in real time using a secure subprocess wrapper with error handling.

Resume Builder: Convert structured task inputs into LaTeX-formatted resume sections and update .tex files automatically.

Real-Time UI: Interactive Streamlit UI with task feedback, multi-column layout, loading bars, and downloadable outputs.

LLM Integration: Modular LLM interface using LiteLLM with OpenRouter API for secure and fast LLM access.

Project Structure
bash
Copy
Edit
taskmaster_ai_crew/
├── agents.py         # CrewAI agents: Planner, Researcher, Executor, Coordinator
├── config.py         # LLM model configuration and routing
├── feedback.py       # Agent feedback and status updates
├── main.py           # Streamlit entrypoint
├── memory.py         # Session memory and state persistence
├── tools.py          # Code execution, ResumeBuilder, and utility tools
├── ui.py             # Streamlit components and layout
├── requirements.txt  # Python dependencies
├── README.md         # Project documentation
├── .env              # API keys and credentials (ignored via .gitignore)
├── .gitignore        # Ignore secrets, models, and output files
Setup Instructions
1. Clone the Repository
bash
Copy
Edit
git clone https://github.com/KRISH7XD/taskmaster_ai_crew.git
cd taskmaster_ai_crew
2. Install Dependencies
Make sure you’re using Python 3.10+.

bash
Copy
Edit
pip install -r requirements.txt
3. Set Environment Variables
Create a .env file for your API keys:

env
Copy
Edit
OPENROUTER_API_KEY=your_openrouter_api_key
LITELLM_MODEL=llama3-70b-instruct
You can also customize the LLM in config.py.

Usage
Launch the Streamlit app:

bash
Copy
Edit
streamlit run main.py
Open http://localhost:8501 in your browser.

Functional Agents
Agent	Role
Planner	Breaks user input into executable task chunks
Researcher	Gathers relevant information using the LLM
Executor	Executes code snippets or structured tasks
Coordinator	Summarizes outputs and gives final feedback
Key Modules
LocalCodeRunner: Safely executes user-defined code with stdout/stderr capture.

ResumeBuilder: Generates custom resume sections in LaTeX format.

feedback.py: Displays live progress updates in UI.

Demo Scenarios
✔️ Build a Resume Section
Input: "Add a section about my internship at Google in AI research."

Output: A .tex block appended to your resume.

⚙️ Run Code on the Fly
Input: "Run this Python snippet: print(2 ** 10)"

Output: 1024

Requirements
Python 3.10+

CrewAI

LiteLLM

Streamlit

OpenRouter API key for LLM access

License
This project is licensed under the MIT License.
© 2025 KRISH7XD

Acknowledgments
CrewAI for agent orchestration

LiteLLM for model abstraction

Streamlit for rapid UI development

LLM API provider: OpenRouter.ai

