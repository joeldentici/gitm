'''
bundle-merge

Updates the remote branches with bundles from reading the configured mailbox
'''

from subprocess import call

'''
bundleMerge :: BundleMerge

Merges a bundle into a branch
'''
def bundleMerge(bundle, error):
	#put bundle onto filesystem
	tmp = bundle.temp()

	#verify that we can merge bundle into the repo
	code = call(['git', 'verify', tmp], shell=True)
	if (code):
		error()

	#merge the bundle into the repo
	code = call(['git', 'fetch', tmp], shell=True)
	if (code):
		error()