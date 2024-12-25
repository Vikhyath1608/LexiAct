from meta_ai_api import MetaAI

ai = MetaAI()
response = ai.prompt(message="What was the Warriors score last game?", stream=True)
for r in response:
    print(r)