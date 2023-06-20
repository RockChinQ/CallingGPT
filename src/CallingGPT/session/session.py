from ..entities.namespace import Namespace
import openai
import logging
import json


class Session:

    namespace: Namespace = None

    messages: list[dict] = []

    model: str = "gpt-3.5-turbo-0613"

    def __init__(self, modules: list, model: str = "gpt-3.5-turbo-0613"):
        self.namespace = Namespace(modules)
        self.model = model

    def ask(self, msg: str) -> dict:
        self.messages.append(
            {
                "role": "user",
                "content": msg
            }
        )

        args = {
            "model": self.model,
            "messages": self.messages,
        }

        if len(self.namespace.functions_list) > 0:
            args['functions'] = self.namespace.functions_list
            args['function_call'] = "auto"

        resp = openai.ChatCompletion.create(
            **args
        )

        logging.debug("Response: {}".format(resp))
        reply_msg = resp["choices"][0]['message']

        ret = {}

        if 'function_call' in reply_msg:

            fc = reply_msg['function_call']
            args = json.loads(fc['arguments'])
            call_ret = self._call_function(fc['name'], args)

            self.messages.append({
                "role": "function",
                "name": fc['name'],
                "content": str(call_ret)
            })

            ret = {
                "type": "function_call",
                "func": fc['name'].replace('-', '.'),
                "value": call_ret,
            }
        else:
            ret = {
                "type": "message",
                "value": reply_msg['content'],
            }

            self.messages.append({
                "role": "assistant",
                "content": reply_msg['content']
            })

        return ret

    def _call_function(self, function_name: str, args: dict):
        return self.namespace.call_function(function_name, args)
    