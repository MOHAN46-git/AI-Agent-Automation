import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import ServerError
import tools

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY or API_KEY == "your_gemini_api_key_here":
    raise ValueError("GEMINI_API_KEY is not configured in .env.")

client = genai.Client(api_key=API_KEY)

TOOL_MAP = {
    "calculate_expression": tools.calculate_expression,
    "read_system_metric": tools.read_system_metric,
    "write_local_log": tools.write_local_log
}

SYSTEM_INSTRUCTION = """
You are an autonomous systems engineering agent.
Deconstruct user objectives into discrete steps, invoke registered tools sequentially,
observe their execution output, and synthesize a final concise status summary.
"""

def generate_with_retry(contents, config, model_name="gemini-3.5-flash", max_retries=4):
    for attempt in range(1, max_retries + 1):
        try:
            return client.models.generate_content(
                model=model_name,
                contents=contents,
                config=config
            )
        except ServerError as e:
            if attempt == max_retries:
                raise
            sleep_sec = attempt * 3
            print(f"    [!] 503 High Demand notice (Attempt {attempt}/{max_retries}). Retrying in {sleep_sec}s...")
            time.sleep(sleep_sec)

def execute_agent_loop(user_goal: str, model_name: str = "gemini-3.5-flash", max_iterations: int = 6):
    print("=" * 70)
    print(f"[*] NEW GOAL: {user_goal}")
    print("=" * 70)

    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=user_goal)]
        )
    ]

    iteration = 0

    while iteration < max_iterations:
        iteration += 1
        print(f"\n--- [AGENT CYCLE {iteration}] ---")

        config = types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            temperature=0.0,
            tools=tools.AGENT_TOOLS
        )

        response = generate_with_retry(contents, config, model_name=model_name)

        candidate = response.candidates[0]
        model_content = candidate.content
        contents.append(model_content)

        function_calls = response.function_calls

        if not function_calls:
            print("\n[+] FINAL AGENT SYNTHESIS:")
            print(response.text)
            return response.text

        response_parts = []
        for call in function_calls:
            fn_name = call.name
            fn_args = dict(call.args) if call.args else {}
            print(f"[*] MODEL ACTION -> Tool Call: {fn_name}({fn_args})")

            if fn_name in TOOL_MAP:
                tool_output = TOOL_MAP[fn_name](**fn_args)
            else:
                tool_output = f"Error: Tool '{fn_name}' does not exist in registry."

            print(f"[+] LOCAL OBSERVATION -> Result: {tool_output}")

            response_parts.append(
                types.Part.from_function_response(
                    name=fn_name,
                    response={"result": tool_output}
                )
            )

        contents.append(
            types.Content(
                role="user",
                parts=response_parts
            )
        )

    print("[!] Maximum iteration threshold reached.")
    return None

if __name__ == "__main__":
    task = (
        "Check the current cpu_load and memory_usage. "
        "Calculate the product of their integer percentage numbers (ignore % symbol). "
        "Log this calculation into 'telemetry_audit.log' with an explanation, and give me a status summary."
    )
    execute_agent_loop(task)
