'''
config

Configure a git repo so it can use gitm
'''

import json
import transports.emailtransport
import transports.fs

transports = {
	'email': transports.emailtransport,
	'fs': transports.fs
}

def add(transportName, remoteName):
	x = None
	try:
		x = getConfig(remoteName)
	except Exception as e:
		pass

	if x:
		raise Exception("Remote already exists")

	config = transports[transportName].config({'remoteName': remoteName})
	config['transportName'] = transportName
	setConfig(remoteName, config)

	print(" ".join(['gitm remote',remoteName,'added with transport:',transportName]))

def update(remoteName):
	config = getConfig(remoteName)
	transportName = config['transportName']

	config = transports[transportName].config(config)

	config['transportName'] = transportName
	setConfig(remoteName, config)
	print(" ".join(['gitm remote',remoteName,'updated']))

def delete(remoteName):
	setConfig(remoteName, None)

def getConfig(remoteName):
	with open('.git/gitm.json') as data:
		return json.load(data)[remoteName]

	raise Exception("Failed to load gitm config")

def setConfig(remoteName, remoteConfig):
	config = {}
	try:
		with open('.git/gitm.json', 'r') as data:
			config = json.load(data)
	except Exception as e:
		config = {}
	if remoteConfig:
		remoteConfig['remoteName'] = remoteName
	config[remoteName] = remoteConfig

	with open('.git/gitm.json', 'w') as f:
		f.write(json.dumps(config, indent=2, sort_keys=True))

def load(remoteName):
	config = getConfig(remoteName)
	transportName = config['transportName']

	return transports[transportName].load(config)