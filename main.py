import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from functions.call_function import available_functions, call_function


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if api_key is None:
    raise RuntimeError("No API key")

client = genai.Client(api_key=api_key)

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true",
                    help="Enable verbose output")
args = parser.parse_args()

messages = [types.Content(
    role="user", parts=[types.Part(text=args.user_prompt)])]


def print_function_call(resp):

    if args.verbose:
        usage = resp.usage_metadata
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {usage.prompt_token_count}")
        print(f"Response tokens: {usage.candidates_token_count}")

        if usage is None:
            raise RuntimeError("No usage")

    function_calls = getattr(resp, "function_calls", None)
    function_results = []

    if function_calls:
        for fc in function_calls:
            function_call_result = call_function(fc, args.verbose)

            if not function_call_result.parts:
                raise Exception

            if not function_call_result.parts[0].function_response:
                raise Exception

            if not function_call_result.parts[0].function_response.response:
                raise Exception

            function_results.append(function_call_result.parts[0])

            if args.verbose:
                print(
                    f"-> {function_call_result.parts[0].function_response.response}")

        return function_results, False

    else:
        print(f"Final Response:\n{resp.text}")
        return [], True


for _ in range(20):
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt)
    )
    if response.candidates:
        for c in response.candidates:
            messages.append(c.content)

    function_results, done = print_function_call(response)
    if done:
        break

    messages.append(types.Content(role="user", parts=function_results))
else:
    print("Stopped after 20 iterations")
    raise SystemExit(1)
