'''
remote-update

Update the remote branches with all bundles in a list of messages.
'''

'''
msgError :: Message -> () -> Exception

Creates an exception for failure to update the repository
'''
def msgError(message):
	num = message.id()
	def error():
		raise Exception('Could not update repo with bundle in message: ' + num)

	return error

'''
remoteUpdate :: (BundleMerge, [Message]) -> ()

Merges bundles into the repository
'''
def remoteUpdate(bundleMerge, messages, remote, branch):
	#merge each message into the remote branch
	for message in messages:
		#get bundle from message and merge it
		bundle = message.bundle()
		bundleMerge(bundle, msgError(message), remote, branch)

		#successfully updated with bundle, so mark as read!
		message.read()