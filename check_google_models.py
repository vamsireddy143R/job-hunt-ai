import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv("server/.env")

api_key = os.getenv("OPENROUTER_API_KEY") # This contains the Google Key
print(f"Key loaded: {api_key[:5]}...")

genai.configure(api_key=api_key)

print("Listing available models...")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")
except Exception as e:
    print(f"Error: {e}")
