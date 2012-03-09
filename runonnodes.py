#!/usr/bin/env python

from noderange import expand
from nodeutils import NodeConnection
import sys
import paramiko
from paramiko import SSHException
import getpass
import argparse

def runonnodes(nodespec, cmd, dshbak=False, verbose=False, user=None):
    nodes = expand(nodespec)

    if len(nodes) == 0:
        print "Need at least one node to run on"
        sys.exit(1)

    for node in nodes:
        nc = NodeConnection(node, user)
        nc.connect(verbose=verbose)
        nc.exec_command(cmd)
        if not dshbak:
            print "--------------- %s ---------------" % (node)
            nc.print_output()
        else:
            nc.print_output(str(node) + ": ")

def main():
    parser = argparse.ArgumentParser(description="Run a command on a set of nodes")
    parser.add_argument('-t', action="store_true", default=False)
    parser.add_argument('-v', action="store_true", default=False)
    parser.add_argument('-w', action="store", dest="where")
    parser.add_argument('-u', action="store", dest="user")
    parser.add_argument('command', nargs='*', action="store")
    args = parser.parse_args(sys.argv[1:])

    runonnodes(args.where, " ".join(args.command), dshbak=args.t, verbose=args.v, user=args.user)

if __name__ == "__main__":
    main()
