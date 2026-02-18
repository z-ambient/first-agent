import os
import subprocess


def run_python_file(working_directory, file_path, args=None):
    try:
        working_path = os.path.abspath(working_directory)

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

        command = ["python3", target_path]
        if args:
            command.extend(args)

        result = subprocess.run(command, cwd=working_path,
                                capture_output=True, text=True, timeout=30)

        output = []

        if result.returncode != 0:
            output.append(f'Process exited with code {result.returncode}')

        if not result.stderr.strip() and not result.stdout.strip():
            output.append('No output produced')
        else:
            if result.stdout:
                output.append(f'STDOUT: {result.stdout}')
            if result.stderr:
                output.append(f'STDERR: {result.stderr}')

        return "\n".join(output)

    except Exception as e:
        return f"Error: executing Python file: {e}"
