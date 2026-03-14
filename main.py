import os
import argparse
from dotenv import load_dotenv
from google import genai

def main():
    load_dotenv()

    try:
        api_key = os.environ.get("GEMINI_API_KEY")
    except KeyError:
        Print("Cannot load API Key")
    except Exception as e:
        print(e)

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    args = parser.parse_args()

    client = genai.Client(api_key=api_key)
    print("Hello from ai-agent!")
    contents = args.user_prompt
    res = client.models.generate_content(model='gemini-2.5-flash', contents=contents)
    tokens_prompt = res.usage_metadata.prompt_token_count
    tokens_response = res.usage_metadata.candidates_token_count
    print(f"User Prompt: {contents}")
    print(f"Prompt tokens: {tokens_prompt}")
    print(f"Response tokens: {tokens_response}")
    print(f"Response: \n{res.text}")



if __name__ == "__main__":
    main()
