import openai
import json
import logging
import os
import sys
import inspect
import re

openai.api_key = os.environ["openai_apikey"]

def draw(prompt: str) -> dict:
    """
    Draw a picture from a prompt using DALL-E.

    Args:
        prompt(str): The prompt to draw from.
    """
    return openai.Image.create(
        prompt=prompt,
    )

def output_img_as_md(img: str) -> str:
    """
    Output an image as Markdown.

    Args:
        img(str): The image to output.
    """
    return "![Generated Image]({})".format(img)

from CallingGPT.entities.namespace import Namespace

ns = Namespace([])

ns.add_function("default", draw)
ns.add_function("default", output_img_as_md)

messages = [
    {
        "role": "user",
        "content": "draw a cat, then convert to markdown"
    }
]


while True:

    resp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        functions=ns.functions_list,
        function_call='auto'
    )

    reply_msg = resp["choices"][0]['message']

    if 'function_call' in reply_msg:
        print("$call fn: {} with {}".format(reply_msg['function_call']['name'], reply_msg['function_call']['arguments']))

        fc = reply_msg['function_call']
        args = json.loads(fc['arguments'])
        call_ret = ns.call_function(fc['name'], args)
        print("$fn ret: {}\n".format(call_ret))

        messages.append({
            "role": "function",
            "name": fc['name'],
            "content": str(call_ret)
        })
    else:
        messages.append({
            "role": "assistant",
            "content": reply_msg
        })

        print("> {}".format(reply_msg['content']))

        break
