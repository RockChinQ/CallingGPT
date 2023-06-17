import openai
import os
import sys


openai.api_key = os.environ["openai_apikey"]

print(openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "user",
            "content": "你好！"
        }
    ]
))
