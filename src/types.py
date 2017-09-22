'''
types

"Types" that are used in the different modules.
'''

'''
Transport :: Object

An object with methods:

config :: (Dict string string) -> Dict string string
Configure a new remote transport. Takes the current settings (if any)
and returns the updated settings after asking user for input on command line

load :: (Dict string string) -> Mailbox
Loads a mailbox for a remote.
'''

'''
Mailbox :: Object

An object with methods:

sendBundle :: Bundle -> Message
Send a git bundle through the transport. Returns the message that it
sends the bundle in.

getUnreadMessages :: () -> [Message]
Gets a list of all unread messages on the mailbox. Transports must guarantee
that no bundle is ever included in this list if it was ever in a message that
has been marked as read. This amounts to making sure read messages are never
included in this list.
'''

'''
Message :: Object

An object with methods:

id :: () -> string
The id of the message in the transport. Typically a UUID.

read :: () -> ()
Marks the message as locally read. We will never
see it again.

bundle :: () -> Bundle
Gets the bundle that was attached to the message
'''

'''
Bundle :: Object

A memory mapped file. Can be easily written to temporary locations
to work with git commands.

Bundle.load :: string -> Bundle
Load bundle from filesystem

Bundle.fromBytes :: [byte] -> Bundle
Load bundle from byte array

Bundle.path :: () -> string
Generates a temporary location in '/tmp' that a bundle can be
written to.

tmp :: () -> string
Write bundle to a location in '/tmp'. Returns the location

bytes :: () -> [byte]
Get the memory mapped byte array.
'''

'''
BundleMerge :: (Bundle, () -> Exception) -> ()

Function that merges a bundle into a branch. Calls the
specified function to raise an exception if it fails.
'''

'''
Merge :: ([string], [string]) -> ()

Function that merges from the left branch into the right
branch. This will raise an error if merging fails.
'''
