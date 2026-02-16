import os
import argparse
from dotenv import load_dotenv
from google import genai


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if api_key is None:
    raise RuntimeError("No API key")

client = genai.Client(api_key=api_key)

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
args = parser.parse_args()

response = client.models.generate_content(
    model='gemini-2.5-flash', contents=args.user_prompt
)

usage = response.usage_metadata


print(f"User prompt: {args.user_prompt}")
print(f"Prompt tokens: {usage.prompt_token_count}")
print(f"Response tokens: {usage.candidates_token_count}")
print(f"Response:\n{response.text}")
