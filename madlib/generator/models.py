import random
from copy import copy
from madlib.generator.tokenizer import MadlibTokenizer

class MarkupException( Exception ):
	pass

class Madlib:
	tokens = []
	
	def parse( self, script ):
		if script.count( '{' ) != script.count( '}' ):
			raise MarkupException( 'Unmatched brackets. You either have too many or not enough {\'s or }\'s.')
		self.tokens = []
		t = MadlibTokenizer()
		t.tokenize( script )
		self.tokens = t.tokens
		
	def generate( self ):
		script = ''
		tokens = copy( self.tokens )

		while len( tokens ):
			token = tokens.pop(0)
			
			# Two possibilities: normal string or group of phrases
			if token == '{':
				# Start parsing phrases
							
				phrases = []
				
				# Store each phrase inside the {}'s
				while 1:
					# Get the phrase
					phrase = tokens.pop(0)
					
					# Parse any subphrases
					if phrase.find( '{' ) >= 0:
						m = Madlib()
						m.parse( phrase )
						phrase = m.generate()
						
					# Store phrase
					phrases += [phrase]
					
					# Get next token (should be '|' or '}')
					token = tokens.pop(0)
					
					# '}' denotes end of phrase group
					if token == '}':
						break
				# Done compiling phrases
				
				# Now choose one
				script += phrases[ random.randint(0, len( phrases ) - 1 ) ]
			else:
				# Just a normal string
				script += token
		return script