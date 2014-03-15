#!/bin/python
import re

file_name = "input_submarine_mips/submarines.s"


class Programa():
	instrucoes = []
	dados = {} 
	rotulo = {}
	memoria_dados=[]

	def __init__(self, file_name):
		self.interpretador()
	
	def interpretador(self):
		file_input = open(file_name).read()
		code = re.sub("(#.*?\n)","\n", file_input)
		code = re.sub("\s{2,}","\n", code)
		code = re.sub("\t"," ", code)
		for line in code.splitlines():
			if(not re.search(":",line) and line):
				self.instrucoes += [Instrucao(line)]
			elif(re.search("(\w+):.*?\.", line)):
				""" ship(nome variaverl): .word(tipo) 320 90 1 4(valores) """
				split = line.split()
				if(not re.search("\"",line)):
					value = list(map(int,re.split(" |:",line)[3:]))
					"""
						Caso esteja no formato submarines: .word -1:500
						500 vetores inicializados com valor -1
					"""
					if(re.search("\d:\d",line)):
						new_value = []
						for i in range(0, value[1]):
							new_value += [value[0]]
						value = new_value
							
				else:
					msg = " ".join(split[2:])[1:-1]
					"""
						Conversao das string normal para 4 letras por posicao(word) 
					"""
					msg = re.findall("(.{3,4})", msg)
					value = msg


				index = len(self.memoria_dados) 
				self.memoria_dados += value
				self.dados[split[0]] = index
			else:
				self.rotulo[line[:-1]] = len(self.instrucoes)
				
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

	
class Dado():
	pass


class Cache():
	pass	
class Memoria():
	pass	

a = Programa(file_name)

print(a.memoria_dados)


