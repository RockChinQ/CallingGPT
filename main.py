import os
import sys
import logging
import yaml
import shutil


def check_config():
    if not os.path.exists('config.yaml'):
        shutil.copyfile('config-template.yaml', 'config.yaml')
        logging.info('config.yaml created. Please edit it and run again.')
        sys.exit(0)

def main():
    pass

if __name__ == '__main__':
    main()