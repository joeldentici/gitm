'''
transports.inputs

Module providing a function to update options
by prompting the user
'''

def textInput(field, msg, value):
	newValue = raw_input('Enter ' + field + ': ' + msg)
	return newValue if newValue else value

import getpass
def passInput(field, msg, value):
	newValue = getpass.getpass('Enter ' + field + ': ' + msg)

	if len(newValue) == 0:
		return value

	confirmValue = getpass.getpass('Confirm ' + field + ': ')

	if confirmValue != newValue:
		print('Passwords do not match')
		return passInput(field, msg, value)

	return newValue if newValue else value

def csvInput(field, msg, value):
	newValue = raw_input('Enter ' + field + ' (comma separated): ' + msg)
	if newValue:
		return map(lambda x: x.strip(), newValue.split(','))
	else:
		return value if value else []

def textOutput(value):
	return '(' + value + ') ' if value else ''

def passOutput(value):
	return textOutput('****' if value else '')

def csvOutput(value):
	return textOutput(", ".join(value))

def intInput(field, msg, value):
	newValue = textInput(field, msg, value)
	try:
		return int(newValue)
	except Exception as e:
		print(str(e))
		return intInput(field, msg, value)


def boolInput(field, msg, value):
	newValue = textInput(field, msg, value)

	if (type(newValue) == bool):
		return newValue

	if newValue.lower() == 'y':
		return True
	elif newValue.lower() == 'n':
		return False
	else:
		print('Must be y/n')
		return boolInput(field, msg, value)

def boolOutput(value):
	return textOutput({
		True: 'y',
		False: 'n'
	}.get(value, ''))

def intOutput(value):
	return textOutput(str(value))

inputMethod = {
	'text': textInput,
	'pass': passInput,
	'csv': csvInput,
	'int': intInput,
	'bool': boolInput
}

outputMethod = {
	'text': textOutput,
	'pass': passOutput,
	'csv': csvOutput,
	'int': intOutput,
	'bool': boolOutput
}

'''
update :: (string, Dict string any, string, string, any) -> ()

Updates the value of the specified option in the specified dictionary.

The user is prompted to enter the specified field value

The user's response is stored into the specified option

If a default option to take the default value from is specified, the
value of that option is used when the specified option value (current) is null
'''
def update(inputType, options, field, option, defaultOption = None):
	#get current value and message
	defaultValue = options[defaultOption] if defaultOption else ''
	value = options.get(option, defaultValue)
	curMsg = outputMethod[inputType](value)

	#prompt for input and update option value
	options[option] = inputMethod[inputType](field, curMsg, value)