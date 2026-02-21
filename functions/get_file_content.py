import os
from google.genai import types

MAX_CHARS = 10000


schema_get_files_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read contents of files in a specified directory relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file you can read",
            ),
        },
    ),
)


def get_file_content(working_directory, file_path):
    try:
        working_directory = os.path.abspath(working_directory)

        target_path = os.path.normpath(
            os.path.join(working_directory, file_path))

        valid_target_path = os.path.commonpath(
            [working_directory, target_path]) == working_directory

        if not valid_target_path:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working_directory'

        if not os.path.isfile(target_path):
            return f'Error: "{file_path}" is not a file'

        with open(target_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)

            extra = f.read(1)

            if extra != "":
                file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                return (file_content_string)

            return (file_content_string)

    except Exception as e:
        return f"Error: {e}"
