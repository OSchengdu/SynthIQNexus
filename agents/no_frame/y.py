import requests
import json
import openai

try:
    # 为了与mofa框架下的.env.secret做区别
    with open(".apikey", "r")  as f:
        config = json.load(f)
        openai.api_key = config["openai_key"]
            
except Exception as e:
        raise RuntimeError(f"failed due to wrong key:{str(e)}")

url = "https://api.siliconflow.cn/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {openai.api_key}",
    "Content-Type": "application/json"
}

def Get(user_input):
    """
    Sends the user's input to the API and returns the model's response.
    """
    payload = {
        "model": "meta-llama/Llama-3.3-70B-Instruct",
        "messages": [
            {
                "role": "user",
                "content": user_input
            }
        ],
        "stream": False,
        "max_tokens": 512,
        "stop": ["null"],
        "temperature": 0.7,
        "top_p": 0.7,
        "top_k": 50,
        "frequency_penalty": 0.5,
        "n": 1,
        "response_format": {"type": "text"}
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"].strip()
    else:
        return f"Error: {response.status_code} - {response.text}"

def Query():
    """
    Continuously prompts the user for input and prints the model's response.
    Stops when the user types ';;;'.
    """
    print("Welcome to the Query & Answer Loop!")
    print("Type ';;;' to end the conversation.\n")
    
    while True:
        # Get user input
        user_input = input("You: ")
        
        # Exit the loop if the user types ';;;'
        if user_input == ";;;":
            print("Goodbye!")
            break
        
        # Get the model's response
        response = Get(user_input)
        
        # Print the model's response
        print(f"AI: {response}\n")

def Debug():
    pass


if name == "main":
    Query()
