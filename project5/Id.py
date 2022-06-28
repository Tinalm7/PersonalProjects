from Core import Core
import sys

class Id:
	
	def parse(self, parser):
		parser.expectedToken(Core.ID)
		self.identifier = parser.scanner.getID()
		parser.scanner.nextToken()
	
	# Called to check if the identifier has been declared
	def semantic(self, parser):
		if parser.nestedScopeCheck(self.identifier)==Core.ERROR:
			print("ERROR: No matching declaration found: " + self.identifier + "\n", end='')
			sys.exit()
	
	# Called by IdList semantic functions to check for doubly declared variables
	def doublyDeclared(self, parser):
		if not parser.currentScopeCheck(self.identifier)==Core.ERROR:
			print("ERROR: Doubly declared variable detected: " + self.identifier + "\n", end='')
			sys.exit()

	# Called by IdList semantic functions to add the variable to the scopes data structure in Parser
	def addToScopes(self, parser, declaredType):
		parser.scopes[-1][self.identifier] = declaredType

	# Called by Assign semantic function to check the declared type of the variable
	def checkType(self, parser):
		return parser.nestedScopeCheck(self.identifier)
	
	def print(self):
		print(self.identifier, end='')

	def addVarInt(self, memory):
		if(len(memory.stack) == 0):
			memory.addToStaticInt(self.identifier)
		else:
			memory.addToStackInt(self.identifier)

	def addVarRef(self, memory):
		if(len(memory.stack) == 0):
			memory.addToStaticRef(self.identifier)
		else:
			memory.addToStackRef(self.identifier)