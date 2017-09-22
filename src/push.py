'''
push

Creates a bundle of differences between the remote branch and the local branch

Updates the necessary remote branch from the mailbox, verifies that the bundle that was created is valid (not fast-forward)
If not, we fail
If so, we update the remote branch with the bundle

If we are still running, we send the bundle to the mailbox


Everything up-to-date
'''
from remote_update import remoteUpdate
from subprocess import call, Popen
import subprocess
from transports.bundle import Bundle

def push(messages, bundleMerge, sendMail, merge, remote, branch):
	#update the repo with bundles
	remoteUpdate(bundleMerge, messages, remote, branch)

	remote = ['gitm', remote, branch]
	remoteBranch = "-".join(remote)

	#get the current commit of the remote branch
	proc = Popen(['git', 'log', '-n', '1', remoteBranch], stdout=subprocess.PIPE)
	commitInfo = proc.stdout.read()
	commit = commitInfo.split('\n')[0].split(' ')[1]

	#merge local branch into remote branch
	merge([branch], remote)


	#create bundle
	bundlePath = Bundle.path()
	bundleDiff = commit + '..' + remoteBranch
	code = call(['git', 'bundle', 'create', bundlePath, bundleDiff])
	if (code):
		raise Exception("Bundle creation failed!")
	
	#load the bundle
	bundle = Bundle.load(bundlePath)

	#send the bundle. mark message as read so we don't look
	#at it if we receive it later
	message = sendMail(bundle)
	message.read()