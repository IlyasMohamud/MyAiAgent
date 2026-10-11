import argparse
import os

from dotenv import load_dotenv
from openai import OpenAI


def main():

    #loading key
    load_dotenv()
    api_key = os.environ.get('OPENROUTER_API_KEY')
    if not api_key: raise RuntimeError("Key not found")

    #take user input
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    #creating client
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key = api_key,
    )

    messages = [
        {"role": "user", "content": args.user_prompt},
    ]

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
    )
    #print output
    if not response.usage:
        raise RuntimeError("failed API request")
    else:
        prompt_tokens = response.usage.prompt_tokens
        response_tokens = response.usage.completion_tokens
    if(args.verbose):
        print(f"User prompt: {args.user_prompt}\nPrompt tokens: {prompt_tokens}\nResponse tokens: {response_tokens}\nResponse: {response.choices[0].message.content}")
    else:
        print(f"Response: {response.choices[0].message.content}")



if __name__ == "__main__":
    main()
