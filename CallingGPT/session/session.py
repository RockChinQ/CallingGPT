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
        resp = openai.ChatCompletion.create(
            model=self.model,
            messages=self.messages,
            functions=self.namespace.functions_list,
            function_call="auto"
        )

        logging.debug("Response: {}".format(resp))
        reply_msg = resp["choices"][0]['message']

        append_msg = {
            "role": "assistant",
        }

        ret = {}

        if 'function_call' in reply_msg:
            fc = reply_msg['function_call']
            args = json.loads(fc['arguments'])
            call_ret = self._call_function(fc['name'], args)

            append_msg['content'] = "(Function: {} called, and returned: {})".format(
                fc['name'],
                call_ret
            )

            ret = {
                "type": "function_call",
                "value": call_ret,
            }
        else:
            append_msg['content'] = reply_msg['content']
            ret = {
                "type": "message",
                "value": reply_msg['content'],
            }

        self.messages.append(append_msg)

        return ret

    def _call_function(self, function_name: str, args: dict) -> dict:
        result = {}

        # split the function name
        module_name, function_name = function_name.split('-')

        # get the function
        function = self.namespace.functions[module_name][function_name]['function']

        # call the function
        result = function(**args)

        return result