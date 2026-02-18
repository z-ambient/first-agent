import os

MAX_CHARS = 10000


def get_file_content(working_path, file_path):
    try:
        working_path = os.path.abspath(working_path)

        target_path = os.path.normpath(
            os.path.join(working_path, file_path))

        valid_target_path = os.path.commonpath(
            [working_path, target_path]) == working_path

        if not valid_target_path:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working_path'

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
