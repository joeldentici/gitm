'''
bundle-merge

Updates the remote branches with bundles from reading the configured mailbox
'''

from subprocess import call

'''
bundleMerge :: BundleMerge

Merges a bundle into a branch
'''
def bundleMerge(bundle, error, remote, branch):
	#put bundle onto filesystem
	tmp = bundle.tmp()

	branch = '-'.join(['gitm', remote, branch])
	branch = branch + ':' + branch

	#verify that we can merge bundle into the repo
	code = call(['git', 'bundle', 'verify', tmp])
	if (code):
		error()

	#merge the bundle into the repo
	code = call(['git', 'fetch', tmp, branch])
	if (code):
		error()