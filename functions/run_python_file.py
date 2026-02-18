import os


def run_python_file(working_directory, file_path, args=None):
    working_path = os.path.abspath(working_path)

    target_path = os.path.normpath(
        os.path.join(working_path, file_path))

    valid_target_path = os.path.commonpath(
        [working_path, target_path]) == working_path

    if not valid_target_path:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(target_path):
        return f'Error: "{file_path}" does not exist or is not a regular file'
 
    if not file_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file'
