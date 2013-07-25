
import json

SHORT_CODE_ALPHABET = "23456789abcdefghijklmnopqrstuvwxyz"

def generateShortCode(givenKey):
	return encode(givenKey)

def createErrorJSON(errorMessage):
	return json.dumps( {"error": errorMessage} )

def createJSON(jsonDict):
	return json.dumps(jsonDict)

def encode(givenKey):

	if (givenKey == 0):
		return SHORT_CODE_ALPHABET[0]

	arr = []
	base = len(SHORT_CODE_ALPHABET)

	while givenKey > 0:
		leftOver = givenKey % base
		givenKey = givenKey // base

		arr.append(SHORT_CODE_ALPHABET[leftOver])

	arr.reverse()
	return ''.join(arr)

def decode(string):
	num = 0
	base = len(SHORT_CODE_ALPHABET)
	for char in string:
		num = num * base + SHORT_CODE_ALPHABET.index(char)
	return num
