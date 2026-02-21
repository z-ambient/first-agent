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
parser.add_argument("--memory", action="store_true",
                    help="Load .agent_memory into context for this run (agent can always write to it)")
args = parser.parse_args()

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
MEMORY_FILE = os.path.join(PROJECT_ROOT, ".agent_memory")

if args.memory and os.path.isfile(MEMORY_FILE):
    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        memory_content = f.read().strip()
    if memory_content:
        system_instruction = f"{system_prompt}\n\nMemory from previous runs:\n{memory_content}"
    else:
        system_instruction = system_prompt
else:
    system_instruction = system_prompt

messages = [types.Content(
    role="user", parts=[types.Part(text=args.user_prompt)])]


def process_response(resp, verbose: bool = False, project_root: str | None = None):
    if verbose:
        usage = getattr(resp, "usage_metadata", None)
        if usage is not None:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {usage.prompt_token_count}")
            print(f"Response tokens: {usage.candidates_token_count}")

    function_calls = getattr(resp, "function_calls", None)
    function_results = []

    if function_calls:
        for fc in function_calls:
            function_call_result = call_function(
                fc, verbose=verbose, project_root=project_root)

            if not function_call_result.parts:
                raise ValueError("Tool returned no parts")

            part = function_call_result.parts[0]

            if not part.function_response:
                raise ValueError("Tool part has no function_response")
            if not part.function_response.response:
                raise ValueError("Tool function_response has no response")

            function_results.append(part)
            if verbose:
                print(f"-> {part.function_response.response}")

        return function_results, False

    return [], True


for _ in range(20):
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_instruction)
    )
    if response.candidates:
        for c in response.candidates:
            messages.append(c.content)

    function_results, done = process_response(
        response, verbose=args.verbose, project_root=PROJECT_ROOT)
    if done:
        final_text = (response.text or "").strip()
        if final_text:
            print(f"Final Response:\n{final_text}")
        else:
            messages.append(types.Content(
                role="user",
                parts=[types.Part(
                    text="In one or two sentences, summarize what you did in this conversation for the user.")],
            ))
            summary_response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=messages,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction),
            )
            if summary_response.candidates and getattr(summary_response, "text", None):
                print(f"Final Response:\n{summary_response.text.strip()}")
            else:
                print("Final Response:\n(no text)")
        break

    messages.append(types.Content(role="user", parts=function_results))
else:
    print("Stopped after 20 iterations")
    raise SystemExit(1)
