from noderange import expand
import sys
import paramiko
from paramiko import SSHException
import getpass

class NodeConnection(object):
    def __init__(self, name, user=None, password=None):
        self.name = name
        self.ssh = None
        self.stdin = None
        self.stdout = None
        self.stderr = None
        if user:
            self.user = user
        else:
            self.user = getpass.getuser()
        self.password = password

    def connect(self, verbose=False, port=22, password_prompt=getpass.getpass):
        if verbose:
            print "Connection to host '%s'" % (self.name)
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        if not self.password:
            try:
                self.ssh.connect(self.name, 22, self.user)
                return
            except SSHException as e:
                # We need a password
                self.password = password_prompt("Key based logon did not work, please provide password for %s@%s: " % (self.user, self.name), stream=sys.stderr)

        self.ssh.connect(self.name, 22, self.user, password=self.password)

    def exec_command(self, cmd):
        if not self.ssh:
            raise Exception("exec_command: not connected")
        self.stdin, self.stdout, self.stderr = self.ssh.exec_command(cmd)

    def print_output(self, leader=''):
        if not self.stdin or not self.stdout or not self.stderr:
            raise Exception("print_output: not connected")
        for line in self.stdout.readlines():
            sys.stdout.write(str(leader) + str(line))
            sys.stdout.flush()
        for line in self.stderr.readline():
            sys.stderr.write(line)
            sys.stderr.flush()

