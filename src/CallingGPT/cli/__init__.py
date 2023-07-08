import logging
import importlib
import json

from ..session.session import Session


def cli_loop(modules: list):

    session = Session(modules)

    cmd = input(">>> ")

    while cmd != "exit":
        if cmd == "help":
            print("help: print this message")
            print("exit: exit the program")
            print("lsf: list all functions")
            print("msg: list all messages")
            print("load: load a module dynamically")
        elif cmd == "lsf":
            print(json.dumps(session.namespace.functions_list, indent=4))
        elif cmd == "msg":
            print(json.dumps(session.messages, indent=4))
        elif cmd == "load":
            module_name = input("module name: ")
            modules = []
            try:
                # delete the .py suffix
                module_name = module_name.replace("/", ".").replace("\\", ".")
                if module_name.endswith('.py'):
                    module_name = module_name[:-3]
                # module = __import__(module_name)
                module = importlib.import_module(module_name)
                print("Using module: {}".format(module.__name__))
                modules.append(module)
            except Exception as e:
                logging.error("Failed to import module {}.".format(module_name))
                logging.error(e)
            session.namespace.add_modules(modules)
        else:
            resp = session.ask(cmd)

            for repl in resp:
                if 'function_call' in repl:
                    print(
                        "call<{}>: {}".format(
                            repl['function_call']['name'],
                            repl['function_call']['arguments']
                        )
                    )
                else:
                    print(
                        "<<< {}".format(
                            repl['content']
                        )
                    )

            # if resp['type'] == 'function_call':
            #     print(
            #         "func<{}>: {}".format(
            #             resp['func'],
            #             resp['value']
            #         )
            #     )
            # elif resp['type'] == 'message':
            #     print(
            #         "<<< {}".format(
            #             resp['value']
            #         )
            #     )

        cmd = input(">>> ")