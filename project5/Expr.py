from Term import Term
from Core import Core

class Expr:
	
	def parse(self, parser):
		self.option = 0
		self.term = Term()
		self.term.parse(parser)
		if parser.scanner.currentToken() == Core.ADD:
			self.option = 1
		elif parser.scanner.currentToken() == Core.SUB:
			self.option = 2
		if not self.option == 0:
			parser.scanner.nextToken()
			self.expr = Expr()
			self.expr.parse(parser)
	
	def semantic(self, parser):
		self.term.semantic(parser)
		if hasattr(self, 'expr'):
			self.expr.semantic(parser)
	
	def print(self):
		self.term.print()
		if self.option == 1:
			print("+", end='')
			self.expr.print()
		elif self.option == 2:
			print("-", end='')
			self.expr.print()

	def execute(self, memory):
		num1 = self.term.execute(memory)
		if self.option == 1:
			num2 = self.expr.execute(memory)
			num1 = num1+num2
		elif self.option == 2:
			num2 = self.expr.execute(memory)
			num1 = num1-num2
		return num1