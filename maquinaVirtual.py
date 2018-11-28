#!/usr/bin/python
# -*- coding: utf-8 -*-
import ast


class maquinaVirtual(object):
    """docstring for sintatico"""
    def __init__(self,lista):

        #Variavel com o nome do arquivo
        self.lista = lista

        self.labels = {}

        self.tabSimbolos = {}

    def setaLabels(self):

        for i in range(0,len(self.lista)):
            if(self.lista[i][0]=='LABEL'):
                self.labels[self.lista[i][1]] = i


    def executacao(self):
        operadores = {
            "-": self.sub,
            "+": self.soma,
            "/": self.divisao,
            "//": self.div,
            "%": self.mod,
            "*": self.mult,
            "=" : self.atrib,
            ">=": self.maiorI,
            "<=": self.menorI,
            "<": self.menor,
            ">": self.maior,
            "==": self.igualdade,
            "!=": self.diferenca,
            "&&": self.funcAND,
            "||": self.funcOR,
            "!": self.funcNOT,
        }
        chamadas = {
            "SCAN": self.scan,
            "PRINT": self.printa
        }
        saltos = {
            "IF": self.funcIF,
            "JUMP": self.funcJUMP
        }
        i=0
        while self.lista[i][1]!='STOP':

            if(self.lista[i][0]=='LABEL'):
                i += 1
                continue

            elif self.lista[i][0] =='IF' or self.lista[i][0] =='JUMP':
                funcao = saltos[self.lista[i][0]]
                i = funcao(self.lista[i][1],self.lista[i][2],self.lista[i][3])
                continue

            elif self.lista[i][0] !='CALL':
                #Seta 'a' e 'b' variavel temporaria como um numero da lista ou variavel da lista
                a,b=0,0
                funcao = operadores[self.lista[i][0]]
                #print(funcao)
                if(type(self.lista[i][2])==int or type(self.lista[i][2])==float):
                    a=self.lista[i][2]
                else:
                    a=self.tabSimbolos[self.lista[i][2]]

                if(type(self.lista[i][3])==int or type(self.lista[i][3])==float):
                    b=self.lista[i][3]
                else:
                    b = self.tabSimbolos[self.lista[i][3]]
                
                self.tabSimbolos[self.lista[i][1]] = funcao(a, b)

            else:
                funcao = chamadas[self.lista[i][1]]
                #print(funcao)
                self.tabSimbolos[self.lista[i][3]] = funcao( self.lista[i][2], self.lista[i][3])

            i+=1

    def soma(self, x, y):
        return x + y

    def sub(self, x, y):
        return x - y

    def divisao(self, x, y):
        return x / y

    def mult(self, x, y):
        return x * y

    def mod(self, x, y):
        return x % y

    def div(self, x, y):
        return x // y

    def atrib(self, x, y):
        return y

    def maiorI(self, x, y):
        return x >= y

    def menorI(self, x, y):
        return x <= y

    def diferenca(self, x, y):
        return x != y

    def maior(self, x, y):
        return x > y

    def menor(self, x, y):
        return x < y

    def igualdade(self, x, y):
        return x == y

    def funcAND(self, x, y):
        return x and y

    def funcOR(self, x, y):
        return x or y

    def funcNOT(self, x, y):
        return not y

    def igualdade(self, x, y):
        return x == y

    def scan(self, x, y):
        if x is not None:
            print(x)
        return float(input(""))

    def printa(self, x, y):
        if x is not None:
            print(str(x))
        if y is not None:
            print(self.tabSimbolos[y])

    def funcIF(self,exp,lab1,lab2):
        print(exp)
        if(exp):
            return self.labels[lab1]
        else:
            return self.labels[lab2]

    def funcJUMP(self,indice,lab1,lab2):
        return self.labels[indice]

if __name__ == '__main__':
    arquivo = open("teste", 'r')
    lista = ast.literal_eval(arquivo.read())

    m = maquinaVirtual(lista)
    m.setaLabels()
    #print(lista)
    m.executacao()
