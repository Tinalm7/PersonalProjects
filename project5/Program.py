from Core import Core
from DeclSeq import DeclSeq
from StmtSeq import StmtSeq

class Program:
	
	def parse(self, parser):
		self.ds = None
		parser.expectedToken(Core.PROGRAM)
		parser.scanner.nextToken()
		if parser.scanner.currentToken() != Core.BEGIN:
			self.ds = DeclSeq()
			self.ds.parse(parser)
		parser.expectedToken(Core.BEGIN)
		parser.scanner.nextToken()
		self.ss = StmtSeq()
		self.ss.parse(parser)
		parser.expectedToken(Core.END)
		parser.scanner.nextToken()
		parser.expectedToken(Core.EOS)
	
	def semantic(self, parser):
		parser.scopes.append({})
		if self.ds != None:
			self.ds.semantic(parser)
		parser.scopes.append({})
		self.ss.semantic(parser)
		parser.scopes.pop()
	
	def print(self):
		print("program\n", end='')
		if self.ds != None:
			self.ds.print(1)
		print("begin\n", end='')
		self.ss.print(1)
		print("end\n", end='')

	def execute(self, memory):
		if self.ds != None:
			self.ds.execute(memory)
		memory.newFrame()
		self.ss.execute(memory)
		memory.exitFrame()
		memory.gcStatic()