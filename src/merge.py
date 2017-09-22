'''
merge

Merges branches of a git repos
'''
from subprocess import call

'''
merge :: Merge

Merges the src branch into the destination branch
'''
def merge(src, dest):
	src = "/".join(src)
	dest = "/".join(dest)

	branch = src + ':' + dest

	code = call(['git', 'fetch', '.', branch], shell=True)

	if (code):
		raise Exception('Merging ' + src + ' into ' + dest + ' failed!')