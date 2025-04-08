import os
import subprocess
from crewai.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults
from config import GITHUB_TOKEN
from github import Github


@tool("TavilySearch")
def tavily_search_tool(query: str) -> str:
    """Searches the web using Tavily and returns up to 3 results."""
    search = TavilySearchResults(max_results=3)  
    return search.invoke(query)


@tool("FileWriter")
def write_to_file(content: str, filename: str = "summary.txt") -> str:
    """Writes content to a file in the output directory."""
    filepath = os.path.join("output", filename)
    os.makedirs("output", exist_ok=True)
    with open(filepath, "w") as f:
        f.write(content)
    return f"Content written to {filepath}"


@tool("CodeExecutor")
def execute_code(code: str) -> str:
    """Executes Python code and returns the output."""
    try:
        from io import StringIO
        import sys
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        
        exec(code)
        output = sys.stdout.getvalue()
        
        sys.stdout = old_stdout
        return f"Code executed successfully:\n{output}"
    except Exception as e:
        return f"Error executing code: {str(e)}"


@tool("GitHubFetcher")
def get_github_repo_info(repo_name: str) -> str:
    """Fetches info about a GitHub repository."""
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(repo_name)
    return f"Repo: {repo.name}, Stars: {repo.stargazers_count}, Description: {repo.description}"


@tool("LocalCodeRunner")
def run_local_code(file_path: str) -> str:
    """Runs code locally based on file extension (e.g., .py, .java, .c, .cpp)."""
    if not os.path.exists(file_path):
        return f"Error: File {file_path} does not exist."

    extension = os.path.splitext(file_path)[1].lower()
    try:
        if extension == ".py":
            result = subprocess.run(["python", file_path], capture_output=True, text=True)
        elif extension == ".java":
            class_name = os.path.splitext(os.path.basename(file_path))[0]
            subprocess.run(["javac", file_path], check=True)
            result = subprocess.run(["java", "-cp", os.path.dirname(file_path), class_name], 
                                  capture_output=True, text=True)
        elif extension == ".c":
            output_file = os.path.splitext(file_path)[0] + ".exe"
            subprocess.run(["gcc", file_path, "-o", output_file], check=True)
            result = subprocess.run([output_file], capture_output=True, text=True)
        elif extension == ".cpp":
            output_file = os.path.splitext(file_path)[0] + ".exe"
            subprocess.run(["g++", file_path, "-o", output_file], check=True)
            result = subprocess.run([output_file], capture_output=True, text=True)
        else:
            return f"Error: Unsupported file extension {extension}. Supported: .py, .java, .c, .cpp"

        if result.returncode == 0:
            return f"Code executed successfully:\nOutput: {result.stdout}"
        else:
            return f"Execution failed:\nError: {result.stderr}"
    except subprocess.CalledProcessError as e:
        return f"Error running code: {str(e)}\nOutput: {e.output}"
    except Exception as e:
        return f"Error: {str(e)}"


@tool("ResumeBuilder")
def build_resume(content: str, filename: str = "resume.txt") -> str:
    """Builds or appends to a resume file, placing project details under 'Projects' section."""
    filepath = os.path.join("output", filename)
    os.makedirs("output", exist_ok=True)
    

    project_content = content.strip()
    
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            existing_content = f.read()

        if "## Projects" in existing_content:

            sections = existing_content.split("## ")
            updated_content = ""
            for i, section in enumerate(sections):
                if section.startswith("Projects"):
                    sections[i] = section.strip() + "\n\n" + project_content
                updated_content += "## " + section if i > 0 else section
        else:

            updated_content = existing_content + "\n\n## Projects\n" + project_content
        
        with open(filepath, "w") as f:
            f.write(updated_content.strip())
        return f"Appended project to {filepath}"
    else:

        resume_template = f"""
# Resume
## Projects
{project_content}

## Skills
- [Add your skills here]
## Experience
- [Add your experience here]
## Education
- [Add your education here]
        """.strip()
        with open(filepath, "w") as f:
            f.write(resume_template)
        return f"Created new resume at {filepath}"


@tool("FileReader")
def read_file(filename: str) -> str:
    """Reads content from a file in the output directory."""
    filepath = os.path.join("output", filename)
    try:
        with open(filepath, "r") as f:
            content = f.read()
        return f"File content:\n{content}"
    except Exception as e:
        return f"Error reading file: {str(e)}"


tools_list = [tavily_search_tool, write_to_file, execute_code, get_github_repo_info, run_local_code, build_resume, read_file]