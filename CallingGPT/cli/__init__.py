import logging

from ..session.session import Session


def cli_loop(modules: list):

    session = Session(modules)

    cmd = input(">>> ")

    while cmd != "exit":
        if cmd == "help":
            print("help: print this message")
            print("exit: exit the program")
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