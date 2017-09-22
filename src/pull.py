'''
pull

Updates the necessary remote branch from mailbox
Tries to merge the remote branch into the corresponding local branch
'''
from remote_update import remoteUpdate

'''
pull :: ([Message], BundleMerge, Merge, string, string) -> ()

Reads the bundle from each message, in order, and attempts to merge
it into the remote branch. If this succeeds for all messages, then
the remote branch is merged into the local branch.
'''
def pull(messages, bundleMerge, merge, remote, branch):
	#print message if we are up to date
	if (len(messages) == 0):
		print("Already up-to-date.")
		return

	remoteUpdate(bundleMerge, messages)

	#attempt to merge the remote branch into local branch
	merge(['gitm', remote, branch], [branch])