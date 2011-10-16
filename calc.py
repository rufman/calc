# Simple Calculator Parser
# FGII, Fall Semester 2007, Simon Bovet
#
# Description:
# This simple calculator parser evaluates any expression
# typed in, and outputs the result.
#
# Example:
#   > 2 + 3 - 1
#   Result: 4

def scanCommand():
	ok, x = scanExpression()
	if ok:
		print "Result:", x

def scanExpression():
	global scanPosition
	
	ok, x = scanTerm()
	if not ok:
		return False, 0

	while True:
		lastPosition = scanPosition
		if scanChar('+'):
			ok, y = scanTerm()
			if ok:
				x = x + y
			else:
				scanPosition = lastPosition
				break
		elif scanChar('-'):
			ok, y = scanTerm()
			if ok:
				x = x - y
			else:
				scanPosition = lastPosition
				break
		else:
			break

	return True, x

def scanTerm():
	global scanPosition
	
	ok, x = scanFactor()
	if not ok:
		return False, 0
	
	while True:
		lastPosition = scanPosition
		if scanChar('x'):
			ok, y = scanFactor()
			if ok:
				x = x * y
			else:
				scanPosition = lastPosition
				break
		else:
			break
	
	return True, x
	
def scanFactor():
	ok, x = scanNumber()
	if ok:
		return True, x
	
	return False, 0

# Return whether the character 'char' could be scanned
def scanChar(char):
	skipWhitespace()
	ok, c = scanChars(char)
	return ok
	
# Return whether any sequence of digits could be scanned,
# together with its numerical value, as an integer number
def scanNumber():
	skipWhitespace()
	ok, c = scanDigit()
	if not ok: return False, 0
	s = ''
	while ok:
		s = s + c
		ok, c = scanDigit()
	return True, int(s)
	
# Return whether any digit could be scanned,
# together with the scanned digit
def scanDigit():
	return scanChars(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])

# Return whether any letter (a, b or c) could be scanned,
# together with the scanned letter
def scanLetter():
	skipWhitespace()
	return scanChars(['a', 'b', 'c'])

# Skip whitespace characters
def skipWhitespace():
	while True:
		ok, c = scanChars([' '])
		if not ok:
			break;

# Return whether any character from the list 'chars' could be scanned,
# together with the scanned character
def scanChars(chars):
	global scannedString, scanPosition
	if scanPosition >= len(scannedString):
		return False, ''
	for c in chars:
		if scannedString[scanPosition] == c:
			scanPosition += 1
			return True, c
	else:
		return False, ''

# Initialize the sttring to be scanned
def setScannedString(string):
	global scannedString, scanPosition
	scannedString = string
	scanPosition = 0
	
# Set the content of variable 'var' to x
def setVariable(var, x):
	global memory
	memory[var] = x
	
# Get the content of variable 'var'
def getVariable(var):
	global memory
	return memory[var]
	
memory = {}

# Main part of the program
print "(Type q to quit)"
while True:
	input = raw_input("> ")		# Prompt user for input
	if input[:1] == 'q':
		break					# Stop if user types 'q'
	elif len(input) > 0:		# If user typed something
		setScannedString(input)
		scanCommand()
