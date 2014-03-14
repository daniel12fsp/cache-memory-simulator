# coding: utf-8

#Memória

# Configurações

TAMANHO_CACHE_L1 = 8
TAMANHO_CACHE_L2 = 32
MAPEAMENTO_DIRETO = True
GRAU_ASSOCIATIVIDADE = 1
PALAVRAS_POR_BLOCO = 1

# Resultados
hitRate = 0
missRate = 0

class Memoria:
	def __init__(self):
		self.memoria = []

	def abrirPrograma(self, programa):
		'''Recebe um programa e cria um espaço virtual para armazenar as linhas.
		O tamanho da memória depende do tamanha do programa'''
		self.memoria = programa
#		for posicao in programa:
#			self.memoria.append(posicao)

	def _lerConteudo(self, endereco, tamanhoBloco):
		'''Retornar um bloco contendo a instrução ou dado em endereco.'''
		missRate += 1 # Adiciona um MISS
		ENDERECO_BLOCO = (endereco/self.tamanhoBloco) * self.tamanhoBloco
		bloco = []
		for i in range(self.tamanhoBloco):
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
		for i in range(tamanho):
			self.cache.append(None)
		self.tamanho = tamanho
		self.associatividade = associatividade
		self.tamanhoBloco = tamanhoBloco
		self.nivelSuperior = None

	def adicionarNivelSuperior(self, cache):
		'''Adiciona uma memória de nível superior à cache.'''
		self.nivelSuperior = cache

	def _buscarBlocoCache(self, endereco):
		'''Busca e retorna o bloco de dados que contem endereco.'''
		ENDERECO_VALIDO = endereco/self.tamanhoBloco
		CONJUNTOS = self.tamanho/self.associatividade

		INDICE = ENDERECO_VALIDO % CONJUNTOS
		TAG = ENDERECO_VALIDO / CONJUNTOS

		if(self.cache[INDICE]):
			for dado in cache[INDICE]:
				if dado[0] == TAG:
					hitRate += 1 # Está na cache, Adiciona um HIT
					return dado[1]
		return self._buscarNivelSuperior() # Não está nesse nível, verifica em nível superior

	def lerCache(self, endereco):
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
		ENDERECO_VALIDO = endereco/self.tamanhoBloco
		CONJUNTOS = self.tamanho/self.associatividade

		INDICE = ENDERECO_VALIDO % CONJUNTOS
		TAG = ENDERECO_VALIDO / CONJUNTOS

		if (MAPEAMENTO_DIRETO): # Apenas mapeamento direto
			self.cache[INDICE] = [(tag, bloco)]
		#TODO: Implementar as outras adições e as políticas de substituição de blocos

def main():
	memoria = Memoria()
	cacheL1 = Cache(TAMANHO_CACHE_L1, GRAU_ASSOCIATIVIDADE, PALAVRAS_POR_BLOCO)
	cacheL2 = Cache(TAMANHO_CACHE_L2, GRAU_ASSOCIATIVIDADE, PALAVRAS_POR_BLOCO)

	cacheL1.adicionarNivelSuperior = cacheL2
	cacheL2.adicionarNivelSuperior = memoria

	#TODO: Loop para o teste manual

if __name__ == "__main__":
	main()
