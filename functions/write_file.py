import os

def write_file(working_directory, file_path, content):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        print(f"{working_dir_abs = }")
        full_path = os.path.join(working_dir_abs, file_path) 
        print(f"{full_path = }")
        target = os.path.normpath(full_path)
        print(f"{target = }")
    except Exception as e:
        return f"Error: {e}"
    
    valid_target = os.path.commonpath([working_dir_abs, target]) == working_dir_abs
    if not valid_target:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if os.path.isdir(file_path):
        return f'Error: Cannot write to "{file_path}" as it is a directory'
    
    try:
        os.makedirs(working_dir_abs, exist_ok=True)
    except Exception as e:
        return f"Error: {e}"
    
    try:
        with open(target, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"