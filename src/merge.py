'''
merge

Merges branches of a git repos
'''
from subprocess import call, Popen
import subprocess

'''
merge :: Merge

Merges the src branch into the destination branch
'''
def merge(src, dest):
	src = "-".join(src)
	dest = "-".join(dest)

	branch = src + ':' + dest


	skip = 'On branch '
	proc = Popen(['git', 'status'], stdout=subprocess.PIPE)
	info = proc.stdout.read()
	info = info[len(skip):]
	curBranch = info[:info.index('\n')]

	args = ['git', 'fetch', '.', branch] if curBranch != dest else ['git', 'merge', src]

	code = call(args)

	if (code):
		raise Exception('Merging ' + src + ' into ' + dest + ' failed!')