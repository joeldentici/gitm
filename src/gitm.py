#!/usr/bin/env python

'''
gitm

Command line tool to push and pull to git repos over an arbitrary transport.

This requires the repository to already be cloned from some normal remote. After that,
this tool will keep track of its own separate remote that operates over a user specified
transport.

This allows extending the capabilities of git beyond ssh and https transports

A transport using email (imap/smtp) is included and is the default. New transports
can be installed by registering the python script implementing them.
'''

import config
import sys

commands = {
	'remote': {
		'add': lambda options: config.add(options[0], options[1]),
		'update': lambda options: config.update(options[0]),
		'delete': lambda options: config.delete(options[0])
	}
}
args = sys.argv[1:]

i = 0
command = commands[args[0]]
while type(command) == dict:
	i = i + 1
	command = command[args[i]]

args = args[i+1:]

try:
	command(args)
except KeyboardInterrupt as e:
	print("")
except Exception as e:
	print str(e)
