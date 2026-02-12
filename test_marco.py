from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:56625/v1",
    api_key="dummy",
)

response = client.chat.completions.create(
    model="marco-o1-q4_k_m",
    messages=[
        {"role": "system", "content": "You are Marco-o1, running on Sol-III."},
        {"role": "user", "content": "Confirm hypercube integration status."}
    ],
)

print(response.choices[0].message.content)
