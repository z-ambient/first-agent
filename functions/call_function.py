import os
from google.genai import types
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_files_content, get_file_content
from functions.write_file import schema_write_file_content, write_file
from functions.run_python_file import schema_run_python_file, run_python_file

schema_write_memory = types.FunctionDeclaration(
    name="write_memory",
    description="Append a short summary to the agent memory file (.agent_memory in the project root) for future runs. Call this when you finish a task so the next run can remember what was done. Appends to the file (adds to existing memory).",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["content"],
        properties={
            "content": types.Schema(
                type=types.Type.STRING,
                description="Summary of what was done (for future runs to remember)",
            ),
        },
    ),
)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_files_content,
        schema_write_file_content,
        schema_run_python_file,
        schema_write_memory,
    ],
)


def call_function(function_call, verbose=False, project_root=None):

    if verbose:
        print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(f" - Calling function: {function_call.name}")

    function_name = function_call.name or ""
    args = dict(function_call.args) if function_call.args else {}

    if function_name == "write_memory":
        if not project_root or not os.path.isdir(project_root):
            function_result = "Error: Project root not available; cannot write memory."
        else:
            memory_path = os.path.join(project_root, ".agent_memory")
            content = args.get("content", "")
            try:
                with open(memory_path, "a", encoding="utf-8") as f:
                    f.write(content)
                    if content and not content.endswith("\n"):
                        f.write("\n")
                function_result = f"Successfully appended to .agent_memory ({len(content)} characters)"
            except Exception as e:
                function_result = f"Error writing .agent_memory: {e}"
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": function_result},
                )
            ],
        )

    function_map = {
        "get_file_content": get_file_content,
        "get_files_info": get_files_info,
        "write_file": write_file,
        "run_python_file": run_python_file,
    }
    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    args["working_directory"] = "./calculator"
    function = function_map[function_name]
    function_result = function(**args)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )
