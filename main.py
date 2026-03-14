import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

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
    res = client.models.generate_content(model='gemini-2.5-flash', contents=messages)
    tokens_prompt = res.usage_metadata.prompt_token_count
    tokens_response = res.usage_metadata.candidates_token_count
    
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {tokens_prompt}")
        print(f"Response tokens: {tokens_response}")
    print(f"Response: \n{res.text}")



if __name__ == "__main__":
    main()
