import os
from google.genai import types
from config import MAX_CHARS

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the contents of a file relative to the permitted working directory, returning up to the maximum allowed number of characters",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to read, relative to the working directory",
            ),
        },
    ),
)

def get_file_content(working_directory, file_path):
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
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target):
        return f'Error: File not found or is not a regular file: "{file_path}"'


    
    try:
        with open(target, "r") as f:
            data = f.read(MAX_CHARS)
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                
            return data
    except Exception as e:
        return f"Error: {e}"
