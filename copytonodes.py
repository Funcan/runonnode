#!/usr/bin/env python

from noderange import expand
from nodeutils import NodeConnection
import sys
import paramiko
from paramiko import SSHException
import getpass
import argparse

def copytonodes(nodespec, srcfile, destfile, verbose=False, user=None):
    nodes = expand(nodespec)

    if len(nodes) == 0:
        print "Need at least one node to run on"
        sys.exit(1)

    if verbose:
        print "Copying from %s to %s" % (srcfile, destfile)

    for node in nodes:
        nc = NodeConnection(node, user)
        nc.connect(verbose=verbose)
        nc.exec_command(cmd)
        nc.print_output()

def main():
    parser = argparse.ArgumentParser(description="Run a command on a set of nodes")
    parser.add_argument('-v', action="store_true", default=False)
    parser.add_argument('-w', action="store", dest="where", required=True)
    parser.add_argument('-u', action="store", dest="user")
    parser.add_argument('src', help='src file')
    parser.add_argument('dest', help='dest file')


    args = parser.parse_args(sys.argv[1:])

    print "args: %s" % (args)
    copytonodes(args.where, args.src, args.dest, verbose=args.v, user=args.user)

if __name__ == "__main__":
    main()
