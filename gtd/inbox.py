#from argparse import ArgumentParser

from sys import argv
from yaml import dump, CDumper, load, CLoader
from os import path

"""
DESCRIPTION
    Submodule for inputing tasks from CLI and uploading from database.

USAGE
    If a task is given, it will be included in the database.
    If a task ID is given, the corresponding task will be printed out.
    If no argument is given, all tasks labeled as 'inbox' will be printed out.
"""

home   = str(path.expanduser('~'))
config_file =  home + '/.gtd/config.yaml'

def get_config(config_file=config_file):
    """
    DESCRIPTION
        Function for loading the configuration stored in a YAML file in ~/.gtd
    """
    with open(config_file) as cf:
        config = load(cf, Loader=CLoader)

    return config

def get_db(config):



#def return_inbox(db):

if __name__ == "__main__":
    print(get_config())


