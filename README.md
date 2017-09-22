# gitm -- Git Message Transport
A script running on top of git that uses git's bundling and fetching from bundle capabilities to do `git push` and `git pull` through an arbitrary transport mechanism, using a message-based protocol.

## How it Works
This simulates normal old https/ssh remotes, but uses arbitrary transports. In the local repo, we keep a copy of remote branches and track them from the local branches.

When a `gitm push` happens, we attempt to update our local copy of the remote branch with the changes that have happened in our local copy of the corresponding local branch. If this is successful, we send the bundle of changes through the transport.

When a `gitm pull` happens, we will update our local remote branches from the bundles in our transport's 'mailbox'. We read all the new messages from our mailbox, and for each, we download the attached bundle. We then apply the bundles in the order received to our remote branches. Now, for the branch included in the `gitm pull`, we try to merge in the remote branch. If this is successful, the `gitm pull` has completed. Otherwise, the user must finish manually merging before it is complete.

## Installation
Run commands below:

```sh
$ wget https://(gitm-host)/gitm-latest.tar.gz
$ tar -xzf gitm-latest.tar.gz
$ cd gitm-latest
$ sudo ./install.sh
```

This will install the `gitm` script and resources into `~/.gitm/` and attempt to link `/bin/gitm` to `~/.git-mail/gitm.py`

## Usage
### To configure a `gitm` remote

```sh
$ gitm remote add <transport> <remote-name>
```

This will set up a new remote in the `gitm` config using the specified transport and the specified name. The transport will prompt for the information it needs.

You can also update an existing `gitm` remote. This causes the transport to prompt for updated values to its config information:
```sh
$ gitm remote update <remote-name>
```

You can remove a remote as well:
```sh
$ gitm remote delete <remote-name>
```

To be able to push and pull a branch to and from the remote, you need to set it up to track the remote:
```sh
$ git checkout <branch-name>
$ gitm track <remote-name>
```

### To pull with `gitm`

```sh
$ gitm pull <remote-name> <branch>
```

This will fetch the latest changes from the mailbox to update the local remote branch and attempt to merge the local remote branch with the local branch.

### To push with `gitm`

```sh
$ gitm push <remote-name> <branch>
```

This will attempt to send a bundle containing the changes between the local branch and the remote branch (after updating the remote branch from the mailbox). If this is a non-fast-forward update, it will fail. In that case, do a `gitm pull` first and merge your branch first.

### To add a new transport
You can add a new transport to `gitm`. This requires registering a python script to manage the transport.

```sh
$ gitm install <transport-name> </path/to/transport.py>
```

Transport installations are global for a given computer. All repos on the computer can use all transports.

## Built-in transports
The following are the built in transports:

* Email (email)