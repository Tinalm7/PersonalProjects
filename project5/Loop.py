from Core import Core
from Cond import Cond
import StmtSeq

class Loop:
	
	def parse(self, parser):
		parser.scanner.nextToken()
		self.cond = Cond()
		self.cond.parse(parser)
		parser.expectedToken(Core.BEGIN)
		parser.scanner.nextToken()
		self.ss = StmtSeq.StmtSeq()
		self.ss.parse(parser)
		parser.expectedToken(Core.ENDWHILE)
		parser.scanner.nextToken()
	
	def semantic(self, parser):
		self.cond.semantic(parser)
		parser.scopes.append({})
		self.ss.semantic(parser)
		parser.scopes.pop()
	
	def print(self, indent):
		for x in range(indent):
			print("\t", end='')
		print("while ", end='')
		self.cond.print()
		print(" begin\n", end='')
		self.ss.print(indent+1)
		for x in range(indent):
			print("\t", end='')
		print("endwhile\n", end='')

	def execute(self, memory):
		while(self.cond.execute(memory)):
			memory.newScope()
			self.ss.execute(memory)
			memory.exitScope()