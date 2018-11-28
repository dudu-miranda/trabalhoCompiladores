class Controle(object):

	def __init__(self):
		self.__tabelasimbolo = {}

	def add_simbolo(self, chave, tipo):
		if(chave in self.__tabelasimbolo.keys()):
			pass
			#Chama erro 
		else:
			self.__tabelasimbolo.update({chave:tipo})

	def verifica_simbolo(self,chave):
		if(chave in self.__tabelasimbolo.keys()):
			return True
		else:
			return False

def aleatorio():
	lista = [1,5,4,3,2]
	lista.extend([])
	print(lista)

aleatorio()

