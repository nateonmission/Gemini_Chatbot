import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from functions.call_functions import available_functions, call_function


def main():
    load_dotenv()

    try:
        api_key = os.environ.get("GEMINI_API_KEY")
    except KeyError:
        Print("Cannot load API Key")
    except Exception as e:
        print(e)
    client = genai.Client(api_key=api_key)
    print("Hello from ai-agent!")


    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    contents = args.user_prompt
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
   
    parser = argparse.ArgumentParser(description="Chatbot")
    res = client.models.generate_content(
        model='gemini-2.5-flash', 
        contents=messages, 
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )
    tokens_prompt = res.usage_metadata.prompt_token_count
    tokens_response = res.usage_metadata.candidates_token_count
    
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {tokens_prompt}")
        print(f"Response tokens: {tokens_response}")
    # print(f"Response: \n{res.text}")
    func_result_list = []
    if res.function_calls is not None:
        for call in res.function_calls:
            print(f"calling Function: {call.name}({call.args})")
            function_call_result = call_function(call, verbose=args.verbose)
            if len(function_call_result.parts) == 0:
                raise Exception("Error: Received no parts from function_call_result")
            
            if call is None:
                raise Exception(f"Error: Received NONE from {call.name}")
            func_result_list.append(function_call_result.parts[0])
            
            
            if call.args.get("verbose"):
                print(f"-> {function_call_result.parts[0].function_response.response}")
    for func_res in func_result_list:
        print(f"{func_res = }")
            


if __name__ == "__main__":
    main()
