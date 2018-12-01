#!/usr/bin/python
# -*- coding: utf-8 -*-


class IO(object):

    """docstring for io"""
    
    def __init__(self, file, other):
        """
        file: Nome do arquivo que contém o código fonte
        """
        #super(io, self).__init__()

        self.Arq = open(file,"r").read()    
        self.ind = 0
        self.tam = len(self.Arq)
        self.__lexico = other 

    def get_char(self):
        """
        Função que retorna um caracter do arquivo fonte
        """
        self.ind += 1
        self.__lexico.aumentaColuna()
        if(self.ind > self.tam):
            return ''

        return self.Arq[self.ind-1]

    def unget_char(self):
        """
        Função que faz o controle do ponteiro do arquivo, reduzindo o índice em 1
        """
        self.__lexico.aumentaColuna(-1)
        self.ind-=1
