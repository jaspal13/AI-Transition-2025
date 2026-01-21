from openai import OpenAI
client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {"role": "system", "content": "You are a helpful AI assistant."},
        {"role": "user", "content": "Who is Jaspal?"}
    ]
)

print(response.choices[0].message.content)