from Decl import Decl
from Func import Func
from Core import Core

class DeclSeq:
	
	def parse(self, parser):
		if(parser.scanner.currentToken() == Core.ID):
			self.funcID=parser.scanner.getID()
			self.func=Func()
			self.func.parse(parser)
		else:
			self.decl = Decl()
			self.decl.parse(parser)
		if not parser.scanner.currentToken() == Core.BEGIN:
			self.ds = DeclSeq()
			self.ds.parse(parser)
	
	def semantic(self, parser):
		if hasattr(self, 'decl'):
			self.decl.semantic(parser)
		if hasattr(self, 'ds'):
			self.ds.semantic(parser)
	
	def print(self, indent):
		if hasattr(self, 'decl'):
			self.decl.print(indent)
		if hasattr(self, 'ds'):
			self.ds.print(indent)

	def execute(self, memory):
		if hasattr(self, 'decl'):
			self.decl.execute(memory)
		elif hasattr(self, 'func'):
			memory.addToStaticFunc(self.funcID, self.func)
		if hasattr(self, 'ds'):
			self.ds.execute(memory)