class Controle(object):

    def __init__(self):
        self.__tabelasimbolo = {}
        self.__auxiliar = self.gerador()

    def add_simbolo(self, chave, tipo):
        if chave in self.__tabelasimbolo.keys():
            return False
        else:
            self.__tabelasimbolo.update({chave: tipo})
        return True

    def verifica_simbolo(self, chave):
        if chave in self.__tabelasimbolo.keys():
            return True
        else:
            return False

    def geraTemp(self):
        return next(self.__auxiliar)

    def gerador(self):
        i = 0
        while True:
            yield i
            i += 1
