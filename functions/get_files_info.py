import os

def get_files_info(working_directory, directory="."):
    working_dir_abs = os.path.abspath(working_directory)
    # print(f"{working_dir_abs = }")
    full_path = os.path.join(working_dir_abs, directory) 
    # print(f"{full_path = }")
    target_dir = os.path.normpath(full_path)
    # print(f"{target_dir = }")

    valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
    if not valid_target_dir:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(target_dir):
        return "Error: The provided path is not a directory."

    lines = []

    for item in os.listdir(target_dir):
        path = os.path.join(target_dir, item)
        file_size = os.path.getsize(path)
        is_dir = os.path.isdir(path)

        lines.append(f"- {item}: file_size={file_size} bytes, is_dir={is_dir}")

    dir_list = "\n".join(lines)
    return dir_list

    
