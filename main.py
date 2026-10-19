import argparse
import json
import os
import sys

from dotenv import load_dotenv
from openai import OpenAI

from call_function import available_functions, call_function
from my_constants import system_runs
from prompts import system_prompt


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
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]
    for _ in range(system_runs):
        response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
            tools=available_functions,
            temperature=0,
        )
        #print output
        if not response.usage:
            raise RuntimeError("failed API request")
        else:
            prompt_tokens = response.usage.prompt_tokens
            response_tokens = response.usage.completion_tokens
            message = response.choices[0].message
            messages.append(message)

        if(message.tool_calls):
            for tool_call in message.tool_calls:
                if(tool_call.type == "function"):
                    function_args = json.loads(tool_call.function.arguments or "{}")
                    #print(f"Calling function: {tool_call.function.name}({function_args})")
                    result_message = call_function(tool_call,args.verbose)
                    messages.append(result_message)
                    if(not result_message["content"]):
                        raise Exception("Empty content")
                    else:
                        if(args.verbose):
                            print(f"-> {result_message['content']}")
        else:
            if(args.verbose):
                print(f"User prompt: {args.user_prompt}\nPrompt tokens: {prompt_tokens}\nResponse tokens: {response_tokens}\nResponse: {response.choices[0].message.content}")
            else:
                print(f"Response: {response.choices[0].message.content}")
            break
    else:
        print(f"System did not finish within {system_runs}")
        sys.exit(1)




if __name__ == "__main__":
    main()
