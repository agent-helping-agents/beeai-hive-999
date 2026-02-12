from langchain_ollama import OllamaLLM

# temperature=0.1 keeps it focused
llm = OllamaLLM(model="tinyllama", temperature=0.1)

bounty_prompt = """
CONTEXT:
In Coolify, 'GenerateDockerCompose' includes all project env vars in one .env file. This is a security leak (#7655).

GOAL:
Provide the PHP code for GenerateDockerCompose.php to:
1. Use $this->resource->environment_variables()->get()
2. Filter variables so only ones belonging to the resource are used.
3. Map them into a 'environment' array instead of 'env_file'.

Show the exact PHP foreach loop and array injection.
"""

print("\n--- [INITIATING BOUNTY ANALYSIS] ---\n")

try:
    response = llm.invoke(bounty_prompt)
    print(response)
    
    # Using a standard string to avoid f-string errors
    with open("suggested_fix.txt", "w") as f:
        f.write(response)
    print("\n--- [SUCCESS: SAVED TO suggested_fix.txt] ---")

except Exception as e:
    print(f"Error: {e}")

