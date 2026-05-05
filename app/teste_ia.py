from app.ai.client import client

resposta = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": "fala oi de forma simpática"}
    ]
)

print(resposta.choices[0].message.content)