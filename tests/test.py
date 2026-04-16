import os
from dotenv import load_dotenv

load_dotenv()

print("Key exists:", bool(os.getenv("OPENAI_API_KEY")))
print("Key prefix:", os.getenv("OPENAI_API_KEY")[:7] if os.getenv("OPENAI_API_KEY") else "Not found")