from StmtSeq import StmtSeq
from Core import Core

class Func:

    def parse(self, parser):
        self.func=parser.scanner.getID()
        parser.scanner.nextToken()
        parser.expectedToken(Core.LPAREN)
        parser.scanner.nextToken()
        parser.expectedToken(Core.REF)
        parser.scanner.nextToken()
        parser.expectedToken(Core.ID)
        self.formals=[]
        self.formals.append(parser.scanner.getID())
        parser.scanner.nextToken()
        while(parser.scanner.currentToken()==Core.COMMA):
            parser.scanner.nextToken()
            parser.expectedToken(Core.ID)
            self.formals.append(parser.scanner.getID())
            parser.scanner.nextToken()
        parser.expectedToken(Core.RPAREN)
        parser.scanner.nextToken()
        parser.expectedToken(Core.BEGIN)
        parser.scanner.nextToken()
        self.stmt=StmtSeq()
        self.stmt.parse(parser)
        parser.expectedToken(Core.ENDFUNC)
        parser.scanner.nextToken()

    def execute(self, memory, formals):
        memory.passParam(formals, self.formals)
        self.stmt.execute(memory)