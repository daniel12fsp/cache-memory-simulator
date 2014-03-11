#!/bin/python
import re

file_name = "input_submarine_mips/submarines.s"


class Programa():
	instrucoes = []

	def __init__(self, file_name):
		self.interpretador()
	
	def interpretador(self):
		file_input = open(file_name).read()
		code = re.sub("(#.*?\n)","", file_input)
		code = re.sub("\s{2,}","\n", code)
		for line in code.splitlines():
			if(not re.search(":",line) and line):
				self.instrucoes += [Instrucao(line)]


	

class Instrucao():
	aritmetica = ["add", "sub", "mult", "div", "mfhi"]
	incondicional_salto = ["jal", "j", "jr", "baq"]
	condicional_salto = ["beq", "bne", "slt", "sltu", "slti", "sltiu", "bgt", "bgtz"]
	memoria = ["li","addi", "lw", "sw", "la", "lhu", "sh", "lb", "lbu", "sb", "ll", "sc", "lui"]
	logica = ["and", "or", "nor", "andi", "ori" , "sll"]

	def __init__(self, line):
		self.line = line
		op = line.split()[0]
		if(op in Instrucao.aritmetica):
			self._type = "Type r"
		elif(op in Instrucao.incondicional_salto):
			self._type = "Type Unconditional jump"
		elif(op in Instrucao.condicional_salto):
			self._type = "Type conditional jump"
		elif(op in Instrucao.memoria):
			self._type = "Type Memory"
		elif(op in Instrucao.logica):
			self._type = "Type Logical"
		elif( op == "blt"):
			self._type = "Pseudo Instrucao"
		else:
			self._type = "Syscam - Desconsidere"

	def __repr__(self):
		return str((self._type, self.line))+"\n"	

	

	
a = Programa(file_name)

print(a.instrucoes)
