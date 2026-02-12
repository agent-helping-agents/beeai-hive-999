from langchain_ollama import OllamaLLM

# Switch to the lightweight model
llm = OllamaLLM(model="tinyllama")

# Refined prompt for TinyLlama
bounty_prompt = """
Target Project: Coolify (PHP/Laravel)
Security Flaw: All project env vars are dumped into a single .env file, leaking secrets between containers.

Objective:
In 'GenerateDockerCompose.php', change the logic to:
1. Stop using a global 'env_file'.
2. Use the 'environment:' section in docker-compose.yml.
3. Map only variables where 'service_id' matches the container.

Provide the PHP code logic to filter these variables.
"""

print("\n--- Running Solver with TinyLlama ---\n")
print(llm.invoke(bounty_prompt))

