class MadlibTokenizer:
	SPECIAL_CHARS = [ '{', '}', '|' ]
	tokens = []
	
	def tokenize( self, script ):
		self.tokens = []
		pointer = 0
		level = 0
		for i,char in enumerate( script ):
			if char in self.SPECIAL_CHARS:
				if char == '{':
					level += 1
					
				if level < 2:
					self.tokens += [script[pointer:i]]
					self.tokens += [char]
					pointer = i + 1

				if char == '}':
					level -= 1
					
		else:
			self.tokens += [script[pointer:i+1]]