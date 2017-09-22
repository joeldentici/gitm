from inputs import update
from bundle import Bundle

import uuid
import json

import smtplib
import email
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email import encoders
import email.header

import imaplib

'''
transports.email

Defines a transport via email

Bundles are sent as emails to a list of recipients

Messages are read from an IMAP server. We locally store a set of
message ids that we have already read, in addition to marking emails
as read on the IMAP server. We always read starting from the latest unread
message with the proper subject and filter any messages that are in the
local set.
'''

GIT = 'GIT BUNDLE['

def setFile(options):
	remote = options['remoteName']
	trans = options['transportName']

	file = '.git/' + trans + '-' + remote + '-read' + '.set'

	return file

def readSetFile(options):
	file = setFile(options)
	try:
		with open(file) as f:
			return set(json.load(f))
	except Exception as e:
		pass

	return set()

def storeSetFile(options, setVal):
	file = setFile(options)

	with open(file, 'w') as f:
		f.write(json.dumps(list(setVal)))

class Message:
	def __init__(self, mailbox, mid, bundle, num = -1):
		if (mid == None):
			mid = str(uuid.uuid4())
		self.mid = mid
		self.mailbox = mailbox
		self._bundle = bundle
		self._subject = None
		self.num = -1

	def bundle(self):
		return self._bundle

	def read(self):
		mailbox = self.mailbox
		try:
			mailbox.conn.store(self.num, '+FLAGS', '\\Seen')
		except Exception as e:
			pass

		mailbox.read.add(self.mid)
		storeSetFile(mailbox.options, mailbox.read)

	def id(self):
		return self.mid

	@staticmethod
	def parseSubject(subject):
		try:
			if subject.startswith(GIT):
				tri = subject[len(GIT):-1]
				return tri.split("/")[0:2]
		except Exception as e:
			pass
		
		return [None, None]

	def subject(self):
		if self._subject:
			return self._subject

		options = self.mailbox.options

		repo = options['repoName']
		mid = self.mid

		info = '/'.join([repo, mid])

		self._subject = GIT + info + ']'

		return self._subject

class EmailMailbox:
	def __init__(self, options):
		self.options = options
		self.read = readSetFile(options)
		self.conn = None

	def sendBundle(self, bundle):
		message = Message(self, None, bundle)
		server = smtplib.SMTP(self.options['smtp'], self.options['smtpPort'])
		if (self.options['smtpEncryption']):
			server.starttls()
		server.login(self.options['smtpUser'], self.options['smtpPassword'])

		def send(to):
			msg = MIMEMultipart()
			msg['From'] = self.options['fromEmail']
			msg['To'] = to
			msg['Subject'] = message.subject()

			print message.subject()

			part = MIMEBase('application', 'octet-stream')
			part.set_payload(message.bundle().bytes())
			encoders.encode_base64(part)
			part.add_header('Content-Disposition', 'attachment; filename= changes.bundle')
			msg.attach(part)

			text = msg.as_string()

			server.sendmail(self.options['fromEmail'], to, text)

		for to in self.options['emailRecipients']:
			send(to)

		return message

	def getUnreadMessages(self):
		def processMessage(num, mid, msg):
			if mid in self.read:
				return

			for part in msg.walk():
				if part.get('Content-Disposition') != None:
					payload = part.get_payload(decode=True)
					bundle = Bundle.fromBytes(payload)
					message = Message(self, mid, bundle, num)
					return message

		if (self.options['imapEncryption']):
			ctor = imaplib.IMAP4_SSL
		else:
			ctor = imaplib.IMAP4

		conn = self.conn = ctor(self.options['imap'])

		conn.login(self.options['imapUser'], self.options['imapPassword'])

		rv, data = conn.select()

		if rv == 'OK':
			rv, data = conn.search(None, '(SUBJECT "' + GIT + '")')
			if (rv != 'OK'):
				return []

			messages = []
			for num in data[0].split():
				rv, data = conn.fetch(num, '(RFC822)')
				if rv != 'OK':
					raise Exception("Cannot read message: " + str(num))
				msg = email.message_from_string(data[0][1])
				decode = email.header.decode_header(msg['Subject'])[0]
				subject = decode[0]

				repo,mid = Message.parseSubject(subject)

				if repo == self.options['repoName']:
					message = processMessage(num, mid, msg)
					if message:
						messages.append(message)

			return messages
		else:
			raise Exception('Cannot open mailbox: ' + str(rv))



def config(options):
	#repo name (so same email can be used w/ multiple repos)
	update('text', options, 'Repository Name', 'repoName')

	#email to send from
	update('text', options, 'Sending Email', 'fromEmail')

	#recipients
	update('csv', options, 'Recipients', 'emailRecipients')

	#update SMTP options
	update('text', options, 'SMTP Server', 'smtp')
	update('text', options, 'SMTP User', 'smtpUser', 'fromEmail')
	update('pass', options, 'SMTP Password', 'smtpPassword')
	update('int', options, 'SMTP Port', 'smtpPort')
	update('bool', options, 'SMTP TLS/SSL (y/n)', 'smtpEncryption')

	#update IMAP options
	update('text', options, 'IMAP Server', 'imap')
	update('text', options, 'IMAP User', 'imapUser', 'smtpUser')
	update('pass', options, 'IMAP Password', 'imapPassword')
	update('int', options, 'IMAP Port', 'imapPort')
	update('bool', options, 'IMAP TLS/SSL (y/n)', 'imapEncryption')

	return options

def load(options):
	return EmailMailbox(options)