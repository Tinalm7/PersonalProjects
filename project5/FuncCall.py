from Core import Core

class FuncCall:

    def parse(self, parser):
        parser.scanner.nextToken()
        parser.expectedToken(Core.ID)
        self.Func = parser.scanner.getID()
        parser.scanner.nextToken()
        parser.expectedToken(Core.LPAREN)
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
        parser.expectedToken(Core.SEMICOLON)
        parser.scanner.nextToken()

    def execute(self, memory):
        memory.newFrame()
        func = memory.getFunc(self.Func)
        func.execute(memory, self.formals)
        memory.exitFrame()

