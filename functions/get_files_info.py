import os


def get_files_info(working_directory, directory="."):
    try:

        working_directory = os.path.abspath(working_directory)

        target_dir = os.path.normpath(
            os.path.join(working_directory, directory))

        valid_target_dir = os.path.commonpath(
            [working_directory, target_dir]) == working_directory

        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        dir_items = os.listdir(target_dir)

        list_of_results = []

        for item in dir_items:
            full_path = os.path.join(target_dir, item)

            size = os.path.getsize(full_path)
            is_file = (os.path.isfile(full_path))
            is_dir = (os.path.isdir(full_path))

            result = f"- {item}: file_size={size} bytes, is_dir={is_dir}"

            list_of_results.append(result)

        return "\n".join(list_of_results)

    except Exception as e:
        return f"Error: {e}"
