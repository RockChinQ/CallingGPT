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
                "func": fc['name'].replace('-', '.'),
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
        fn_spt = function_name.split('-')
        module_name = '-'.join(fn_spt[:-1])
        function_name = fn_spt[-1]

        # get the function
        function = self.namespace.functions[module_name][function_name]['function']

        # call the function
        result = function(**args)

        return result