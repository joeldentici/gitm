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
from pull import pull
from push import push
from bundle_merge import bundleMerge
from merge import merge
from subprocess import call,Popen
import subprocess

def runPull(options):
	remote,branch = options
	transport = config.load(remote)
	messages = transport.getUnreadMessages()
	pull(messages, bundleMerge, merge, remote, branch)

def runPush(options):
	remote,branch = options
	transport = config.load(remote)
	messages = transport.getUnreadMessages()
	sendMail = lambda bundle: transport.sendBundle(bundle)
	push(messages, bundleMerge, sendMail, merge, remote, branch)

def runTrack(options):
	remote, = options
	skip = 'On branch '
	proc = Popen(['git', 'status'], stdout=subprocess.PIPE)
	info = proc.stdout.read()
	info = info[len(skip):]
	branch = info[:info.index('\n')]

	newBranch = '-'.join(['gitm', remote, branch])

	call(['git', 'checkout', '-b', newBranch])
	call(['git', 'checkout', branch])

commands = {
	'remote': {
		'add': lambda options: config.add(options[0], options[1]),
		'update': lambda options: config.update(options[0]),
		'delete': lambda options: config.delete(options[0])
	},
	'pull': runPull,
	'push': runPush,
	'track': runTrack
}
args = sys.argv[1:]

try:
	i = 0
	command = commands[args[0]]
	while type(command) == dict:
		i = i + 1
		command = command[args[i]]

	args = args[i+1:]
except Exception as e:
	print("Invalid arguments. See documentation for proper usage.")
	sys.exit(1)

try:
	command(args)
except KeyboardInterrupt as e:
	print("")
except Exception as e:
	print(str(e))
	sys.exit(1)
