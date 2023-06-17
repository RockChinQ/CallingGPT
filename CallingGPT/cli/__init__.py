import logging
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
        elif cmd == "lsf":
            print(json.dumps(session.namespace.functions_list, indent=4))
        else:
            resp = session.ask(cmd)

            if resp['type'] == 'function_call':
                print(
                    "func<{}>: {}".format(
                        resp['func'],
                        resp['value']
                    )
                )
            elif resp['type'] == 'message':
                print(
                    "<<< {}".format(
                        resp['value']
                    )
                )

        cmd = input(">>> ")