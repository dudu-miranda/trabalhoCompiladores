from copy import deepcopy


class Controle(object):

    def __init__(self):
        self.__tabelasimbolo = {}
        self.__auxiliar = self.gerador()
        self.__auxiliar2 = self.gerador2()
        self.__auxiliarBloco = self.geradorBloco()

    def add_simbolo(self, chave, tipo, bloco):
        """
        :param chave: nome da variavel
        :param tipo: tipo da variavel
        :param bloco: bloco da declaracao
        :return:
        """
        if bloco in self.__tabelasimbolo.keys():
            if chave in self.__tabelasimbolo[bloco].keys():
                return False
        else:
            self.__tabelasimbolo.update({bloco: {}})

        self.__tabelasimbolo[bloco].update({chave: tipo})
        return True

    def verifica_simbolo(self, chave, listablocos):
        """
        :param chave: Nome da variavel
        :param listablocos: lista com os blocos onde pode estar a variavel
        :return: True se achou
        """
        listablocos = deepcopy(listablocos)
        listablocos.reverse()
        for bloco in listablocos:
            if bloco not in self.__tabelasimbolo.keys():
                continue
            if chave in self.__tabelasimbolo[bloco].keys():
                return bloco

        return False

    def geraTemp(self):
        return '__temp' + str(next(self.__auxiliar))

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

    def geradorBloco(self):
        i = 0
        while True:
            yield i
            i += 1

    def gerabloco(self):
        return "Bloco_" + str(next(self.__auxiliarBloco))
