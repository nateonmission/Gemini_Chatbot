import os
import subprocess
from google.genai import types


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file located within the permitted working directory and returns its stdout and stderr output",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional list of command-line arguments to pass to the Python script",
            ),
        },
    ),
)


def run_python_file(working_directory, file_path, args=None):
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
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target):
        return f'Error: "{file_path}" does not exist'
    if file_path[-2:]!="py":
        return f'Error: "{file_path}" is not a Python file'
    
    command = ["python", full_path]
    
    if args:
        for arg in args:
            command.extend(arg)
    try:
        res = subprocess.run(command, cwd=working_dir_abs, capture_output=True, text=True, timeout=30)
    except Exception as e:
        return f"Error: {e}"
    
    if res.returncode != 0:
        return f"Error: Process exited with code {res.returncode}"
    if not res.stdout and not res.stderr:
        return f"Error: No output produced"
    
    output_string = f"STDOUT: {res.stdout}\nSTDERR: {res.stderr}"
    
    return output_string
    