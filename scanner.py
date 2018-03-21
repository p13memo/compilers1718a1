"""
Script to recognize if input time is in valid form by table drive.
Time in valid form means:
-- Hours: [0-23] with 1 or 2 digits
-- Splitter: '.' or ':'
-- Minutes: [0-59] always with 2 digits
"""

# Original source: https://www.pythoncentral.io/how-to-check-if-a-string-is-a-number-in-python-including-unicode/
def is_number(s):
	""" returns 'd' if char is a number, otherwise returns character 'o' """

	try:
		float(s)
		return 'd';
	except ValueError:
		pass
 
	try:
		import unicodedata
		unicodedata.numeric(s)
		return 'd'
	except (TypeError, ValueError):
		pass
 
	return 'o'

def getchar(words,pos):
	""" returns char at pos of words, or None if out of bounds """

	if pos<0 or pos>=len(words): return None

	# If splitter is found, return character 's'.
	if words[pos]=='.' or words[pos]==':':
		return 's'
	# Else return 'd' for numbers or 'o' for other characters
	else:
		return is_number(words[pos])
	

def scan(text,transition_table,accept_states):
	""" Scans `text` while transitions exist in 'transition_table'.
	After that, if in a state belonging to `accept_states`,
	returns the corresponding token, else ERROR_TOKEN.
	"""
	
	# initial state
	pos = 0
	state = 'q0'
	
	while True:
		
		c = getchar(text,pos)	# get next char
		
		if state in transition_table and c in transition_table[state]:
		
			# Check if first digit of minutes is smaller than 6.
			# Acceptable values are [0-6]
			if state=='q3' and 0 <= float(text[pos]) < 6:
				state = transition_table[state][c]	# set new state
				pos += 1	# advance to next char
			# When you get a second digit for hours you must check if the total number is acceptable
			# If previous number was smaller than 2, any digit is acceptable
			# If previous number is equal to 2, only digits 0-3 are acceptable
			elif state=='q1' and c!='s' and ( (float(text[pos-1]) < 2) or (float(text[pos-1]) == 2 and float(text[pos]) < 4) ):
				state = transition_table[state][c]	# set new state
				pos += 1	# advance to next char
			elif state=='q1' and c=='s':
				state = transition_table[state][c]	# set new state
				pos += 1	# advance to next char
			elif state!='q3' and state!='q1':
				state = transition_table[state][c]	# set new state
				pos += 1	# advance to next char
			else:
				# current state is not accepting
				return 'ERROR_TOKEN',pos
			
		else:	# no transition found

			# check if current state is accepting
			if state in accept_states:
				return accept_states[state],pos

			# current state is not accepting
			return 'ERROR_TOKEN',pos
			
	
# the transition table, as a dictionary
td = { 'q0':{ 'd':'q1'},  # initial state
       'q1':{ 'd':'q2','s':'q3'},  # hour's first (and maybe the only one) digit
       'q2':{ 's':'q3' },  # hour's second digit if it exists
       'q3':{ 'd':'q4'},  # splitter
       'q4':{ 'd':'q5'}   # minutes' first digit
     } 

# the dictionary of accepting states and their
# corresponding token
ad = { 'q5':'TIME_TOKEN'  # minutes' second digit
     }

# Open Log File
mylogfile = 'history.log'
f = open(mylogfile, 'a')

# get a string from input
text = input('give some input>')
f.write('give some input>' + text + '\n')  # Log

# scan text until no more input
while text:	# that is, while len(text)>0
	
	# get next token and position after last char recognized
	token,position = scan(text,td,ad)
	
	if token=='ERROR_TOKEN':
		print(token,": time in invalid form.")
		f.write(token + ": time in invalid form." + '\n')  # Log
		break
	
	print("token:",token,"string:",text[:position])
	f.write("token: " + token + " string: " + text[:position] + '\n')  # Log
	
	# remaining text for next scan
	text = text[position:]
	f.close()
	