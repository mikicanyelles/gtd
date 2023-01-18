#from argparse import ArgumentParser

from sys import argv
from yaml import dump, CDumper, load, CLoader
from os import path

from paramiko import SSHClient, AutoAddPolicy

from time import time

"""
DESCRIPTION
    Submodule for inputing tasks from CLI and uploading from database.

USAGE
    If a task is given, it will be included in the database.
    If a task ID is given, the corresponding task will be printed out.
    If no argument is given, all tasks labeled as 'inbox' will be printed out.
"""

gtd_path    = str(path.expanduser('~')) + '/.gtd/'
config_file = gtd_path + '/.gtd/config.yaml'


def ssh_connect(config):

    # Create SSH object
    ssh = SSHClient()
    ssh.set_missing_host_key_policy(AutoAddPolicy())

    if 'password' in list(config.keys()):
        ssh.connect(
            config['hostname'],
            username=config['user'],
            password=config['password'],
            port=config['port']
        )

    elif 'ssh_key' in list(config.keys()):
        ssh.connect(
            config['hostname'],
            username=config['username'],
            key_filename=config['ssh_key'],
            port=config['port']
        )

    return ssh

def get_config(config_file=config_file):
    """
    DESCRIPTION
        Function for loading the configuration stored in a YAML file in ~/.gtd
    """
    with open(config_file) as cf:
        config = load(cf, Loader=CLoader)

    return config

def get_db(config):

    ssh = ssh_connect(config)

    db_file   = gtd_path + config['db_path'].split('/')[-1]
    timestamp = round(time())

    ## Stablish SFTP protocol and get file
    sftp = ssh.open_sftp()
    sftp.get(config['db_path'], db_file + '.' + str(timestamp))
    sftp.close()


    with open(db_file) as f:
        db = load(f, Loader=CLoader)

    return db, db_file, timestamp

def compare_dbs():
    """
    DESCRIPTION
        Function for comparing recently downloaded dbs with stored (not uploaded) dbs.

        If the offline version is newer, replace it by the recently downloaded.
    """

def add_task():
    """
    DESCRIPTION
        Function for adding a task to GTD
    """









#def return_inbox(db):

if __name__ == "__main__":
    config = get_config()
    get_db(config)


