#!/bin/python
import re

#file_name = "input_submarine_mips/submarines.s"

class Programa():
	def __init__(self, file_name):
		self.instrucoes = []
		self.programa = []
		self.fim_programa = 0
		self.dados = {} 
		self.rotulo = {}
		self.memoria_dados=[]
		self.interpretador(file_name)

	def interpretador(self, file_name):
		file_input = open(file_name).read()
		code = re.sub("(#.*?\n)","\n", file_input) # Retirar comentarios
		code = re.sub("\s{2,}","\n", code) # Retirar espacos extras
		code = re.sub("\t"," ", code) # Retirar a tabulacao
		for line in code.splitlines():
			if(not re.search(":",line) and not re.search(".data",line) and not re.search(".text",line) and line):
				self.instrucoes += [line]
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
					msg = re.findall("(.{1,})", msg)
					value = msg

				index = len(self.memoria_dados) 
				self.memoria_dados += value
				self.dados[split[0]] = index
			else:
				self.rotulo[line[:-1]] = len(self.instrucoes)
		self._compilarPrograma()

	def _compilarPrograma(self):
		for instrucao in self.instrucoes:
			string_linha = instrucao
			string_linha = string_linha.replace(',',' ')
			linha = string_linha.split()
			self.programa.append(linha)
		self.fim_programa = len(self.programa)
		self.programa.extend(self.memoria_dados)
		for dado in self.dados:
			self.dados[dado] += self.fim_programa
