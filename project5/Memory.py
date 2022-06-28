from Scanner import Scanner
from Func import Func
from Core import Core
import sys

# Parser class contains all the persistent data structures we will need, and some helper functions
class CoreVar:
	def __init__(self, varType, value):
		self.varType=varType
		self.value=value

class Memory:
	
	#Constructor for Memory
	def __init__(self, inputFile):
		self.static={}
		self.staticFunc={}
		self.stack=[]
		self.currentFrame=-1
		self.heap=[]
		self.refCount=[]
		self.input = Scanner(inputFile)

	def addToStaticInt(self, name):
		self.static[name]=CoreVar("Int", 0)

	def addToStaticRef(self, name):
		self.static[name]=CoreVar("Ref", None)

	def addToStaticFunc(self, name, func):
		self.staticFunc[name]=CoreVar("Func", func)

	def newFrame(self):
		self.stack.append([])
		self.currentFrame+=1
		self.newScope()

	def exitFrame(self):
		self.exitScope()
		self.stack.pop()
		self.currentFrame-=1

	def newScope(self):
		self.stack[self.currentFrame].append({})

	def exitScope(self):
		index=len(self.stack[self.currentFrame])-1
		while len(self.stack[self.currentFrame][index])>0:
			var=self.stack[self.currentFrame][index].popitem()[1]
			if(var.varType=="Ref" and not var.value==None):
				#print("var.value:"+str(var.value))
				self.refCount[var.value]-=1
				if(self.refCount[var.value]==0):
					print("gc:"+str(var.value))
					self.refCount.pop(var.value)
					self.heap.pop(var.value)
		self.stack[self.currentFrame].pop()

	def gcStatic(self):
		while len(self.static)>0:
			var=self.static.popitem()[1]
			if(var.varType=="Ref" and not var.value==None):
				#print("var.value:"+str(var.value))
				self.refCount[var.value]-=1
				if(self.refCount[var.value]==0):
					print("gc:"+str(var.value))
					self.refCount.pop(var.value)
					self.heap.pop(var.value)

	def addToStackInt(self, name):
		index=len(self.stack[self.currentFrame])-1
		self.stack[self.currentFrame][index][name]=CoreVar("Int", 0)

	def addToStackRef(self, name):
		index=len(self.stack[self.currentFrame])-1
		self.stack[self.currentFrame][index][name]=CoreVar("Ref", None)

	def inputToId(self, id):
		if(self.input.token==Core.EOS):
			print("ERROR: input file does not have enough values")
			sys.exit()
		val = self.input.getCONST()
		self.input.nextToken()
		self.getVar(id).value=val

	def getIdVal(self, id):
		val=0
		var = self.getVar(id)
		if(var.varType=="Int"):
			val=var.value
		elif(var.varType=="Ref"):
			val=self.heap[var.value]
		return val

	def getVar(self, id):
		varFound = False
		increment = (len(self.stack[self.currentFrame])-1)
		var=None
		while((varFound==False) and (increment>=0)):
			if(id in self.stack[self.currentFrame][increment]):
				varFound=True
				var=self.stack[self.currentFrame][increment][id]
			increment-=1
		if(varFound==False):
			if(id in self.static):
				var=self.static[id]
		return var

	def getFunc(self, id):
		if(id in self.staticFunc):
			return self.staticFunc[id].value
		else:
			print("ERROR: function not declared")
			sys.exit


	def getVarPrevFrame(self, id):
		varFound = False
		increment = (len(self.stack[self.currentFrame-1])-1)
		var=None
		while((varFound==False) and (increment>=0)):
			if(id in self.stack[self.currentFrame-1][increment]):
				varFound=True
				var=self.stack[self.currentFrame-1][increment][id]
			increment-=1
		if(varFound==False):
			if(id in self.static):
				var=self.static[id]
		return var

	def updateInt(self, id, value):
		self.getVar(id).value=value

	def updateRef(self, id, value):
		index=self.getVar(id)
		if(index.value==None):
			print("ERROR: cannot update a null pointer")
			sys.exit()
		else:
			self.heap[index.value]=value

	def shareRef(self, id1, id2):
		var1=self.getVar(id1)
		var2=self.getVar(id2)
		if(not var1.value==None):
			self.refCount[var1.value]-=1
		var1.value=var2.value
		if(not var2.value==None):
			self.refCount[var2.value]+=1

	def newClass(self, id):
		self.heap.append(0)
		self.refCount.append(1)
		self.getVar(id).value=(len(self.heap)-1)
		print("gc:"+str(len(self.refCount)))

	def passParam(self, param1, param2):
		increment=0
		while(increment<len(param2)):
			self.addToStackRef(param2[increment])
			if(increment>=len(param1)):
				print("ERROR: invalid number of parameters")
				sys.exit()
			var2=self.getVar(param2[increment])
			var2.value=self.getVarPrevFrame(param1[increment]).value
			self.refCount[var2.value]+=1
			increment+=1

