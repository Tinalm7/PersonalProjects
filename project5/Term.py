from Factor import Factor
from Core import Core

class Term:
	
	def parse(self, parser):
		self.factor = Factor()
		self.factor.parse(parser)
		if parser.scanner.currentToken() == Core.MULT:
			parser.scanner.nextToken()
			self.term = Term()
			self.term.parse(parser)
	
	def semantic(self, parser):
		self.factor.semantic(parser)
		if hasattr(self, 'term'):
			self.term.semantic(parser)
	
	def print(self):
		self.factor.print()
		if hasattr(self, 'term'):
			print("*", end='')
			self.term.print()

	def execute(self, memory):
		val = self.factor.execute(memory)
		if hasattr(self, 'term'):
			val = val * self.term.execute(memory)
		return val