import os
import sys
import logging
import yaml
import shutil
import openai
import importlib

from src.CallingGPT.cli import cli_loop


logging.basicConfig(level=logging.INFO)


def check_config():
    if not os.path.exists('config.yaml'):
        shutil.copyfile('config-template.yaml', 'config.yaml')
        logging.info('config.yaml created. Please edit it and run again.')
        sys.exit(0)

def main():
    # read openai.api_key from config.yaml
    check_config()
    cfg = yaml.load(open('config.yaml', 'r'), Loader=yaml.FullLoader)
    openai.api_key = cfg['openai']['api_key']

    # read modules from os.argv
    modules = []

    for module_name in sys.argv[1:]:
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
            sys.exit(1)

    if len(modules) == 0:
        logging.warning("No module imported, you're in normal chat mode.")

    cli_loop(modules)


if __name__ == '__main__':
    main()