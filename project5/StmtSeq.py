from Assign import Assign
from Input import Input
from Output import Output
from If import If
from Loop import Loop
from Decl import Decl
from FuncCall import FuncCall
from Core import Core
import sys

class StmtSeq:

	def parse(self, parser):
		if parser.scanner.currentToken() == Core.ID:
			self.stmt = Assign()
		elif parser.scanner.currentToken() == Core.INPUT:
			self.stmt = Input()
		elif parser.scanner.currentToken() == Core.OUTPUT:
			self.stmt = Output()
		elif parser.scanner.currentToken() == Core.IF:
			self.stmt = If()
		elif parser.scanner.currentToken() == Core.WHILE:
			self.stmt = Loop()
		elif parser.scanner.currentToken() == Core.INT or parser.scanner.currentToken() == Core.REF:
			self.stmt = Decl()
		elif parser.scanner.currentToken() == Core.BEGIN:
			self.func = FuncCall()
			self.func.parse(parser)
		else:
			print("ERROR: Bad start to statement: " + parser.scanner.currentToken().name + "\n", end='')
			sys.exit()
		if(hasattr(self, 'stmt')):
			self.stmt.parse(parser)
		if (not parser.scanner.currentToken() == Core.END
			and not parser.scanner.currentToken() == Core.ENDIF
			and not parser.scanner.currentToken() == Core.ENDWHILE
			and not parser.scanner.currentToken() == Core.ELSE
			and not parser.scanner.currentToken() == Core.ENDFUNC):
			self.ss = StmtSeq()
			self.ss.parse(parser)
	
	def semantic(self, parser):
		if hasattr(self, 'func'):
			print()
		else:
			self.stmt.semantic(parser)
		if hasattr(self, 'ss'):
			self.ss.semantic(parser)
	
	def print(self, indent):
		if hasattr(self, 'func'):
			print()
		else:
			self.stmt.print(indent)
		if hasattr(self, 'ss'):
			self.ss.print(indent)

	def execute(self, memory):
		if hasattr(self, 'func'):
			self.func.execute(memory)
		else:
			self.stmt.execute(memory)
		if hasattr(self, 'ss'):
			self.ss.execute(memory)