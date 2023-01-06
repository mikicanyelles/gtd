from getpass import getpass
from os import path
from sys import exit

"""
TODO
    - [] Save config as yaml in local. Add SSH or local
    - [] create db in local
    - [] Encryption of config.yaml in local
    - []
"""


def ssh_config_creator(verbose=False):
    """
    DESCRIPTION
        Function for configuring GTD with the DB in a SSH server. It will create a dictionary:
            info :
                hostname
                user
                password/ssh_key
                port
                db_path
    """

    def ask_ssh():
        from os import environ

        current_user = environ.get("USER")
        if current_user == '':
            current_user = environ.get("USERNAME")

        info = {}
        info['hostname'] = input("Hostname or IP: ")
        info['user']     = input("User name [%s]: " % current_user)
        if info['user'] == '':
            info['user'] = current_user
            print("User is configured as \033[1m%s\033[0m." % info['user'])

        if verbose == True:
            info['password'] = getpass("Password or route for using SSH keys (file existance will be checked): ")
        elif verbose == False:
            info['password'] = getpass("Password or route for using SSH keys: ")

        if path.exists(info['password']):
            info['ssh_key'] = info['password']
            del info['password']

        info['port']     = input("Port [22]: ")
        if info['port'] == '':
            info['port'] = "22"

        info['db_path']  = input("Database path in sever [~/.gtd/]: ")
        if info['db_path'] == '':
            info['db_path'] = '~/.gtd/'
        elif str(info['db_path'])[-1] != '/':
            info['db_path'] = info['db_path'] + '/'

        return info

    def check_ssh(info, create_db=True):
        """
        DESCRIPTION
            Checks SSH connection and creates gtd.db file in specified route.
        """
        from paramiko import SSHClient,AutoAddPolicy

        ssh = SSHClient()
        ssh.set_missing_host_key_policy(AutoAddPolicy())

        if 'password' in list(info.keys()):
            ssh.connect(
                info['hostname'],
                username=info['user'],
                password=info['password'],
                port=info['port']
            )

        elif 'ssh_key' in list(info.keys()):
            ssh.connect(
                info['hostname'],
                username=info['username'],
                key_filename=info['ssh_key'],
                port=info['port']
            )

        if create_db == True:
            stdin, stdout, stderr = ssh.exec_command("mkdir -p %s; touch %sgtd.db" % (info['db_path'], info['db_path']))
            ssh.close()
            del ssh, stdin, stdout, stderr
            return "Successful connection and gtd.db created"
        elif create_db == False:
            stdin, stdout, stderr = ssh.exec_command("echo")
            ssh.close()
            del ssh, stdin, stdout, stderr
            return "Successful connection"


    def save_config(info, config_file='config.yaml'):

        from os import mkdir
        from yaml import dump, Dumper

        text = dump(info, Dumper=Dumper)

        pr = input("Do you want to print the file to check if the info is correct (Y/n)? ")
        if pr.lower() in ('', 'yes', 'y'):
            print(text)
        elif pr.lower() in ('no', 'n'):
            pass
        else :
            pass

        try :
            mkdir('~/.gtd')
        except FileExistsError:
            pass

        if path.exists('~/.gtd/' + config_file):
            overwrite = input("%s already exists, interrupt the execution and rename the file to keep it. Press RETURN to overwrite it.")
            if overwrite == '':
                config_file = open('~/.gtd/' + config_file)
                config_file.write(text)
                config_file.close()

                return "Config file successfully overwritten in ~/.gtd."

        else :
            config_file = open('~/.gtd/' + config_file)
            config_file.write(dump(info, Dumper=Dumper))
            config_file.close()

            return "Config file successfully saved in ~/.gtd."



    print("Let's start configuring the SSH connection to file.")
    if verbose == True:
        print("Parameters for SSH connection will be asked, SSH connection will be tested and DB file will be created in server. A config file will be created in a default (~/.gtd/) or in a user-specified route containing this information and it will be encrypted for higher security.")


    info = ask_ssh()
    print(info)
    print("Checking SSH connection and creating gtd.db file...")
    ssh_out = check_ssh(info)
    print(ssh_out)
    print("SSH connection works, saving configuration...")
    save_config(info)


if __name__ == '__main__':
    ssh_config_creator()
    exit()





