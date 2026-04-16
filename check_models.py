from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

models = client.models.list()

print("\n--- AVAILABLE MODELS ---\n")

for m in models.data:
    print(m.id)