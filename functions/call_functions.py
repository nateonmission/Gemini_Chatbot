from google.genai import types
from .get_files_info import schema_get_files_info
from .get_file_content import schema_get_file_content
from .run_python_file import schema_run_python_file
from .write_file import schema_write_file
from .get_file_content import get_file_content
from .get_files_info import get_files_info
from .write_file import write_file
from .run_python_file import run_python_file

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ],
)

def call_function(function_call:types.FunctionCall, verbose=False):
    if verbose:
        print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(f" - Calling function: {function_call.name}")
    
    function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "write_file": write_file,
        "run_python_file": run_python_file,
    }
    
    function_name = function_call.name or ""
    if function_name not in function_map.keys():
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
        
    args = dict(function_call.args) if function_call.args else {}
    
    args["working_directory"] = "./calculator"
    
    res = function_map[function_name](**args or "")
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": res},
            ),
        ],
    )