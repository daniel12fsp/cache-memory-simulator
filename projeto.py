# coding: utf-8

from instrucao import Programa

#Memória

# Configurações

TAMANHO_CACHE_L1 = 8 # Posições
TAMANHO_CACHE_L2 = 32
MAPEAMENTO_DIRETO = True
GRAU_ASSOCIATIVIDADE = 1
PALAVRAS_POR_BLOCO = 4

# Resultados
hitRate = 0
missRate = 0

REGISTRADORES = ['$zero',
	'$at',
	'$v0', '$v1',
	'$a0', '$a1', '$a2', '$a3',
	'$t0', '$t1', '$t2', '$t3', '$t4', '$t5', '$t6', '$t7',
	'$s0', '$s1', '$s2', '$s3', '$s4', '$s5', '$s6', '$s7',
	'$t8', '$t9',
	'$k0', '$k1',
	'$gp',
	'$sp',
	'$fp',
	'$ra']

arquivo = 'teste.asm'

class Memoria:
	def __init__(self):
		self.memoria = []
	
	def imprimirMemoria(self):
		print('Memória\nEnd*.:\tValor:')
		for end in range(len(self.memoria)):
			print('%s\t%s' % (end, self.memoria[end]))
		print('*Endereço virtual. (endereço_real/4)\n')

	def _abrirPrograma(self, programa):
		'''Recebe um programa e cria um espaço virtual para armazenar as linhas.
		O tamanho da memória depende do tamanha do programa'''
		self.memoria = programa
#		for posicao in programa:
#			self.memoria.append(posicao)

	def _lerConteudo(self, endereco, tamanhoBloco):
		'''Retornar um bloco contendo a instrução ou dado em endereco.'''
		global missRate
		missRate += 1 # Adiciona um MISS
		ENDERECO_BLOCO = int(endereco/tamanhoBloco) * tamanhoBloco
		bloco = []
		for i in range(tamanhoBloco):
			try:
				bloco.append(self.memoria[ENDERECO_BLOCO + i])
			except:
				bloco.append(None)
		return bloco

class Cache:
	'''Formato da cache: [conj_1, conj_2, ..., conj_k] k = TAMANHO_CACHE/GRAU_ASSOCIATIVIDADE
	Formato dos conjuntos: [dado_1, dado_2, ..., dado_n], n = GRAU_ASSOCIATIVIDADE
	Formato dos dados: (tag, bloco de dados)
	Formato dos blocos de dados: [palavra_1, palavra_2, ..., palavra_i], i = PALAVRAS_POR_BLOCO'''
	def __init__(self, tamanho, associatividade, tamanhoBloco):
		self.cache = []
		self.cache.extend([None]*tamanho)
		self.tamanho = tamanho
		self.associatividade = associatividade
		self.tamanhoBloco = tamanhoBloco
		self.nivelSuperior = None

	def adicionarNivelSuperior(self, cache):
		'''Adiciona uma memória de nível superior à cache.'''
		self.nivelSuperior = cache

	def imprimirMemoria(self):
		self.nivelSuperior.imprimirMemoria()

	def _buscarBlocoCache(self, endereco):
		'''Busca e retorna o bloco de dados que contem endereco.'''
		ENDERECO_VALIDO = int(endereco/self.tamanhoBloco)
		CONJUNTOS = int(self.tamanho/self.associatividade)

		INDICE = ENDERECO_VALIDO % CONJUNTOS
		TAG = int(ENDERECO_VALIDO / CONJUNTOS)

		if(self.cache[INDICE]):
			for dado in self.cache[INDICE]:
				if dado[0] == TAG:
					global hitRate
					hitRate += 1 # Está na cache, Adiciona um HIT
					return dado[1]
		return self._buscarNivelSuperior(endereco) # Não está nesse nível, verifica em nível superior
	
	def _abrirPrograma(self, programa):
		self.nivelSuperior._abrirPrograma(programa)

	def ler(self, endereco):
		'''Interface principal. Retorna o dado do endereço de memória.'''
		bloco = self._buscarBlocoCache(endereco)
		return bloco[endereco % self.tamanhoBloco]

	def _buscarNivelSuperior(self, endereco):
		'''Busca e retorna o bloco que contem endereco no nível superior depois de adiciona este bloco neste nível.'''
		if (type(self.nivelSuperior) == Cache):
			bloco = self.nivelSuperior._buscarBlocoCache(endereco)

		if (type(self.nivelSuperior) == Memoria):
			bloco = self.nivelSuperior._lerConteudo(endereco, self.tamanhoBloco)

		self._adicionarBlocoCache(bloco, endereco)
		return bloco

	def _adicionarBlocoCache(self, bloco, endereco):
		'''Adiciona um bloco de dados nesse nível de cache.'''
		ENDERECO_VALIDO = int(endereco/self.tamanhoBloco)
		CONJUNTOS = int(self.tamanho/self.associatividade)

		INDICE = ENDERECO_VALIDO % CONJUNTOS
		TAG = int(ENDERECO_VALIDO / CONJUNTOS)

		if (MAPEAMENTO_DIRETO): # Apenas mapeamento direto
			self.cache[INDICE] = [(TAG, bloco)]
		#TODO: Implementar as outras adições e as políticas de substituição de blocos

class Processador:
	def __init__(self):
		self.ativo = False
		self.pc = 0
		self.memoria = None
		self.programa = None
		self.registradores = {}
		self.instrucoes = {
			'add': self._add,
			'addi': self._addi,
			'move': self._move,
			'sub': self._sub,
			'subi': self._subi,
			'mul': self._mul,
			'div': self._div,
			'slt': self._slt,
			'slti': self._slti,
			'j': self._j,
			'jal': self._jal,
			'jr': self._jr,
			'beq': self._beq,
			'bne': self._bne,
			'lw': self._lw,
			'sw': self._sw,
			'la': self._la,
			'syscall': self._syscall}

		for reg in REGISTRADORES:
			self.registradores[reg] = 0

	def adicionarMemoria(self, memoria):
		'''Adiciona a memória cache de no primeiro nível.'''
		self.memoria = memoria

	def adicionarPrograma(self, programa):
		'''Adiciona um programa a ser executado.'''
		self.programa = programa

	def imprimirRegistradores(self):
		'''Imprime os registradores e seus valores.'''
		print('Registradores\nReg.:\tValor:')
		for reg in REGISTRADORES:
			print('%s\t%s' % (reg, self.registradores[reg]))
		print('\n')

	def imprimirMemoria(self):
		'''Imprime os valores em memória.'''
		self.memoria.imprimirMemoria()

	def _abrirPrograma(self, programa):
		self.memoria._abrirPrograma(programa)

	def _ler(self, endereco):
		return self.memoria.ler(endereco)

	def executar(self):
		'''Executa um programa.'''
		# Configurar pilha, frame, PC, IR
		program_compilado = self.programa.programa
		fim_programa = self.programa.fim_programa * 4
		tam_pilha = 32 # Escolhi 32 apenas para termos um espaço razoável em pilha
		program_compilado.extend([None]*tam_pilha)
		end_pilha = (len(program_compilado) - 1) * 4
		self.registradores['$sp'] = end_pilha
		self._abrirPrograma(program_compilado)
		self.ativo = True
		while (self.ativo and self.pc != fim_programa):
			try:
				instrucao = self._ler(int(self.pc/4))
				self.pc += 4
				self.instrucoes[instrucao[0]](instrucao[1:])
			except IndexError:
				self.ativo = False
				print("ERRO: Segmentation fault. Impossível executar instrução na posição de memoria %s." % (int(self.pc/4)))
				raise

	# Implementação das Instruções

	# Aritméticas
	def _add(self, parametros):
		self.registradores[parametros[0]] = (self.registradores[parametros[1]] +
			self.registradores[parametros[2]])

	def _addi(self, parametros):
		self.registradores[parametros[0]] = self.registradores[parametros[1]] + int(parametros[2])

	def _move(self, parametros):
		self.registradores[parametros[0]] = self.registradores[parametros[1]]

	def _sub(self, parametros):
		self.registradores[parametros[0]] = (self.registradores[parametros[1]] -
			self.registradores[parametros[2]])

	def _subi(self, parametros):
		self.registradores[parametros[0]] = self.registradores[parametros[1]] - int(parametros[2])

	def _mul(self, parametros):
		self.registradores[parametros[0]] = (self.registradores[parametros[1]] *
			self.registradores[parametros[2]])

	def _div(self, parametros):
		self.registradores[parametros[0]] = int(self.registradores[parametros[1]] /
			self.registradores[parametros[2]])

	# Logicas
	def _slt(self, parametros):
		if(self.registradores[parametros[1]] < self.registradores[parametros[2]]):
			self.registradores[parametros[0]] = 1
		else:
			self.registradores[parametros[0]] = 0

	def _slti(self, parametros):
		if(self.registradores[parametros[1]] < int(parametros[2])):
			self.registradores[parametros[0]] = 1
		else:
			self.registradores[parametros[0]] = 0

	# Saltos
	def _j(self, parametros):
		self.pc = int(parametros[0])

	def _jal(self, parametros):
		self.registradores['$ra'] = self.pc
		self.pc = int(parametros[0])

	def _jr(self, parametros):
		self.pc = self.registradores[parametros[0]]

	# Desvios
	def _beq(self, parametros):
		if(self.registradores[parametros[0]] == parametros[1]):
			self.pc = self.programa.rotulo[parametros[1] + ':'] * 4

	def _bne(self, parametros):
		if(self.registradores[parametros[0]] != parametros[1]):
			self.pc = self.pc + parametros[2] - 4

	# Acesso a Memória
	def _lw(self, parametros):
		split = parametros[1].split('(',1)
		reg = split[1].split(')',1)[0]
		constante = int(split[0])
		if(not constante):
			constante = 0

		endereco = self.registradores[reg] + constante
		self.registradores[parametros[0]] = self._ler(int(endereco/4))

	def _sw(self, parametros):
		pass

	def _la(self, parametros):
		self.registradores[parametros[0]] = self.programa.dados[parametros[1] + ':'] * 4

	# Syscall
	def _syscall(self, object):
		codigo = self.registradores['$v0']
		if codigo == 1: # imprime um inteiro, $a0 = valor
			print(self.registradores['$a0'])
		elif codigo == 4: # imprime uma string, $a0 = endereço da string
			endereco = int(self.registradores['$a0']/4)
			print(self.programa.programa[endereco])
		elif codigo == 5: # lê um inteiro, $v0 = valor lido
			num = int(input())
			self.registradores['$v0'] = num
		elif codigo == 10: # Fim do programa
			self.ativo = False

def main():
	memoria = Memoria()
	cacheL1 = Cache(TAMANHO_CACHE_L1, GRAU_ASSOCIATIVIDADE, PALAVRAS_POR_BLOCO)
	cacheL2 = Cache(TAMANHO_CACHE_L2, GRAU_ASSOCIATIVIDADE, PALAVRAS_POR_BLOCO)

	cacheL1.adicionarNivelSuperior(cacheL2)
	cacheL2.adicionarNivelSuperior(memoria)

	processador = Processador()
	processador.adicionarMemoria(cacheL1)

	programa = Programa('teste.asm')

	processador.adicionarPrograma(programa)
	processador.executar()
	processador.imprimirRegistradores()
	processador.imprimirMemoria()
	
	print('Configuração da Arquitetura\nTamanho da Cache L1 = %d (posições)\nTamanho da Cache L2 = %d (posições)\nMapeamento direto = %r\nGrau de Associatividade = %d\nPalavras por bloco = %d\n' %
		(TAMANHO_CACHE_L1, TAMANHO_CACHE_L2, MAPEAMENTO_DIRETO, GRAU_ASSOCIATIVIDADE, PALAVRAS_POR_BLOCO))
	global hitRate, missRate
	total = (hitRate + missRate)
	print('Resultados\nHit Rate: (%d) %.1f%% \tMiss Rate: (%d) %.1f%%' % (hitRate, hitRate/total*100, missRate, missRate/total*100))
	#TODO: Loop para o teste manual

if __name__ == "__main__":
	main()
