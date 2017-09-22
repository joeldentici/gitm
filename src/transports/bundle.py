import uuid

class Bundle:
	def __init__(self, data):
		self.data = data

	@staticmethod
	def load(path):
		with open(path, 'rb') as f:
			return Bundle.fromBytes(f.read())

	@staticmethod
	def fromBytes(data):
		return Bundle(data)

	@staticmethod
	def path():
		return '/tmp/' + str(uuid.uuid4()) + '.bundle'


	def tmp(self):
		path = Bundle.path()
		with open(path, 'wb') as f:
			for byte in self.data:
				f.write(byte)
		return path

	def bytes(self):
		return self.data