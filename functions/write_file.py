import os


def write_file(working_directory, file_path, content):
    try:
        working_directory = os.path.abspath(working_directory)

        target_path = os.path.normpath(
            os.path.join(working_directory, file_path))

        valid_target_path = os.path.commonpath(
            [working_directory, target_path]) == working_directory

        if not valid_target_path:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if os.path.isdir(target_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        parent_dir = os.path.dirname(target_path)

        if parent_dir:
            os.makedirs(parent_dir, exist_ok=True)

        with open(target_path, "w", encoding="utf-8") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"
