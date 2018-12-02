class Controle(object):

    def __init__(self):
        self.__tabelasimbolo = {}
        self.__auxiliar = self.gerador()
        self.__auxiliar2 = self.gerador2()

    def add_simbolo(self, chave, tipo):
        if chave in self.__tabelasimbolo.keys():
            return False
    
        self.__tabelasimbolo.update({chave: tipo})
        return True

    def verifica_simbolo(self, chave):
        if chave in self.__tabelasimbolo.keys():
            return True
        else:
            return False

    def geraTemp(self):
        return '__temp'+str(next(self.__auxiliar))

    def gerador(self):
        i = 0
        while True:
            yield i
            i += 1

    def geraLabel(self):
        return '__label'+str(next(self.__auxiliar2))

    def gerador2(self):
        i = 0
        while True:
            yield i
            i += 1
