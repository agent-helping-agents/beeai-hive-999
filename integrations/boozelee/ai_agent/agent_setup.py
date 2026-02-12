import subprocess
from camel.agents import ChatAgent
from camel.models import ModelFactory

# Terminal Tool
def run_cmd(command):
    return subprocess.getoutput(command)

# Setup Gemini
gemini_model = ModelFactory.create(
    model_platform="google",
    model_type="gemini-1.5-flash",
)

# Setup Agent
agent = ChatAgent(
    system_message="You are a Termux assistant. Use the 'gh' CLI for GitHub tasks.",
    model=gemini_model,
)

# Task
response = agent.step("List files in current directory using 'ls'")
print(response.msg.content)

