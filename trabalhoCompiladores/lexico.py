#!/usr/bin/python
# -*- coding: utf-8 -*-

import trabalhoCompiladores.entradasaida as entradasaida
import re
from trabalhoCompiladores.enumTkn import enumTkn


class lexico(object):
    

    """docstring for lexico"""
    def __init__(self, file):
        """
        file:nome do arquivo com o codigo fonte
        """
        #Expressão regular dos numeros
        self.er_num = re.compile(r'[0-9]')
        #Expressão regular das letras
        self.er_letra = re.compile(r'[a-z]|[A-Z]')
        #Expressão regular dos numeros e letras
        self.er_num_letra = re.compile(r'[a-z]|[A-Z]|[0-9]')
        #Variavel que contem o lexema atual
        self.lexema = ''
        #Variavel que contem o token atual
        self.token_atual = 0
        #Variavel que manterá uma instancia do objeto de entrada e saida
        self.arquivo = entradasaida.IO(file, self)
        #Variavel que guardará a coluna
        self.__col = 1
        #Variavel que guardará a linha
        self.__linha = 1

    @property
    def coluna(self):
        """
        Propiedade que retorna a coluna atual do ponteiro no arquivo fonte
        """
        return self.__col-len(self.lexema)
        
    @property
    def linha(self):
        """
        Propiedade que retorna a linha
        """
        return self.__linha

    def aumentaColuna(self, qnt = 1):
        self.__col += qnt

    def aumentaLinha(self, qnt = 1):
        """
        qnt: a quantidade a ser acrescida ao contador de linha
        """
        self.__linha += qnt
        self.__col = 1

    def temporario(self):
        token=None
        while token != enumTkn.tkn_eof:
            token = self.getToken()
            print("coluna: %d Linha: %d" %(self.coluna, self.__linha))
            print("%s %s" %(token, self.lexema) )

    def getToken(self):
        """
        Retorna o proximo token encontrado no arquivo fonte
        """
        estado=1 
        string=''
        char=self.arquivo.get_char()

        while True:
            #Estado inicial
            if(estado==1):
                # tratamento de comentario
                if char == '/':
                    char = self.arquivo.get_char()
                    if char == '/':
                        while self.arquivo.get_char() != '\n':
                            pass
                        self.aumentaLinha()   
                        continue
                    elif char == '*':
                        while True:
                            char = self.arquivo.get_char()
                            if char == '*':
                                if self.arquivo.get_char() == '/':
                                    break
                            elif char == '\n':
                                self.aumentaLinha()
                        char = self.arquivo.get_char()
                        continue
                    else:
                        char = '/'
                #Tratamento da virgula
                if(char==','):
                    self.lexema=','
                    self.token_atual = enumTkn.tkn_virg
                    return enumTkn.tkn_virg
                #Tratamento do ponto e virgula
                elif(char==';'):
                    self.lexema=';'
                    self.token_atual = enumTkn.tkn_ptVirg
                    return enumTkn.tkn_ptVirg
                #Tratamento do abre parenteses
                elif(char=='('):
                    self.lexema='('
                    self.token_atual = enumTkn.tkn_abrePar
                    return enumTkn.tkn_abrePar    
                #Tratamento do fecha parenteses
                elif(char==')'):
                    self.lexema=')'
                    self.token_atual = enumTkn.tkn_fechaPar
                    return enumTkn.tkn_fechaPar
                #Inicio do tratamento da multiplicação/potenciacao
                elif(char=='*'):
                    self.lexema='*'
                    self.token_atual = enumTkn.tkn_mult
                    return enumTkn.tkn_mult
                #Tratamento da adicao    
                elif(char=='+'):
                    self.lexema='+'
                    self.token_atual = enumTkn.tkn_add
                    return enumTkn.tkn_add
                #Tratamento da subtracao    
                elif(char=='-'):
                    self.lexema='-'
                    self.token_atual = enumTkn.tkn_sub
                    return enumTkn.tkn_sub
                #Tratamento da divisao
                elif(char=='/'):
                    self.lexema='/'
                    self.token_atual = enumTkn.tkn_div
                    return enumTkn.tkn_div
                #Tratamento do modulo
                elif(char=='%'):
                    self.lexema='%'
                    self.token_atual = enumTkn.tkn_mod
                    return enumTkn.tkn_mod
                #Tratamento de abrir chaves
                elif(char=='{'):
                    self.lexema='{'
                    self.token_atual = enumTkn.tkn_abreCha
                    return enumTkn.tkn_abreCha
                #Tratamento de fechar chaves
                elif(char=='}'):
                    self.lexema='}'
                    self.token_atual = enumTkn.tkn_fechaCha
                    return enumTkn.tkn_fechaCha


                ######################## Dificuldade agora XD #############################


                #Tratamento do menor que,maior que, diferente igualdade, e os outros
                elif(char=='<' or char=='>' or char=='!' or char=='='):
                    string = char
                    char = self.arquivo.get_char()
                    #Inicio do tratamento dos tokens, diferença, igualdade, menor igual, maior igual
                    if(char=='='):
                        #token menor ou igual
                        if(string=='<'):
                            self.token_atual = enumTkn.tkn_menorI
                        #Token maior ou igual
                        elif(string=='>'):
                            self.token_atual = enumTkn.tkn_maiorI
                        #Token igualdade
                        elif(string=='='):
                            self.token_atual = enumTkn.tkn_igualdade
                        #Token diferença
                        elif(string=='!'):
                            self.token_atual = enumTkn.tkn_maiorI                    
                        
                    #Tratamento dos tokens not, atribuicao, menor que, maior que
                    else:
                        self.arquivo.unget_char()
                        char=''
                        #Token not
                        if(string=='!'):
                            self.token_atual = enumTkn.tkn_not
                        #Token atrib
                        elif(string=='='):
                            self.token_atual = enumTkn.tkn_atrib
                        #Token menor que
                        elif(string=='<'):
                            self.token_atual = enumTkn.tkn_menorQ
                        #Token maior que
                        elif(string=='>'):
                            self.token_atual = enumTkn.tkn_maiorQ


                    self.lexema=string+char    
                    return self.token_atual    


                elif(char=='|' or char=='&'):
                    if(self.arquivo.get_char()==char):
                        if(char=='|'):
                            self.token_atual = enumTkn.tkn_or
                        else:
                            self.token_atual = enumTkn.tkn_and
                        self.lexema = char+char
                    else:
                        break    

                    return self.token_atual


                #Inicio do tratamento de variavel/print/scan/while/if/else/break/continue/for/int/float
                elif(self.er_letra.match(char)!=None):
                    estado=2
                    string+=char

                #Inicio do tratamento de numeros    
                elif(self.er_num.match(char)!=None):
                    string+=char
                    estado=3

                #Inicio do tratamento das strings
                elif(char=='\"'):
                    estado=5

                elif(char==''):
                    lexema=''
                    self.token_atual = enumTkn.tkn_eof
                    return enumTkn.tkn_eof
                #Tratamento de espaço no texto
                elif(char==' '):
                    pass
                elif(char=='\n'):
                    self.aumentaLinha()
                elif(char=='\t'):
                    self.aumentaColuna(4)
                else:
                    break    


            #Restante do tratamento das variaveis e palavras reservadas    
            elif(estado==2):
                if(self.er_num_letra.match(char)!=None):
                    string+=char
                else:    
                    self.arquivo.unget_char()
                    
                    self.lexema=string

                    if(string=='print'):
                        self.token_atual = enumTkn.tkn_out
                    elif(string=='scan'):
                        self.token_atual = enumTkn.tkn_in
                    elif(string=='int'):
                        self.token_atual = enumTkn.tkn_int
                    elif(string=='float'):
                        self.token_atual = enumTkn.tkn_float
                    elif(string=='break'):
                        self.token_atual = enumTkn.tkn_break
                    elif(string=='continue'):
                        self.token_atual = enumTkn.tkn_continue
                    elif(string=='for'):
                        self.token_atual = enumTkn.tkn_for
                    elif(string=='while'):
                        self.token_atual = enumTkn.tkn_while
                    elif(string=='if'):
                        self.token_atual = enumTkn.tkn_if
                    elif(string=='else'):
                        self.token_atual = enumTkn.tkn_else
                    elif(string=='return'):
                    	self.token_atual = enumTkn.tkn_return
                    else:
                        self.token_atual = enumTkn.tkn_var
                    return self.token_atual


            #Restante do tratamento dos numeros        
            elif(estado==3):
                if(self.er_num.match(char)!=None):
                    string+=char
                elif(char=='.'):    
                    string+=char
                    estado=4
                else:
                    self.arquivo.unget_char()
                    self.lexema=string
                    self.token_atual = enumTkn.tkn_numInt
                    return enumTkn.tkn_numInt

            elif(estado==4):
                if(self.er_num.match(char)!=None):
                    string+=char
                else:
                    self.arquivo.unget_char()
                    self.lexema=string+'0'
                    self.token_atual = enumTkn.tkn_numFloat
                    return enumTkn.tkn_numFloat
                    

            #Restante do tratamento das strings
            elif(estado==5):
                if(char!='\"'):
                    if(char == '\\'):

                        if(self.arquivo.get_char() == 'n'):
                            string += '\n'
                        elif(self.arquivo.get_char() == 't'):
                            string += '\t'
                        else:
                            string+=char
                            string+=self.arquivo.get_char()
                    else:
                        string+=char
                else:
                    self.lexema=string
                    self.token_atual = enumTkn.tkn_str
                    return enumTkn.tkn_str    

            #Caso de leitura
            char=self.arquivo.get_char()
            


        #Return para caso de um erro léxico da linguagem
        return -1


if __name__ == '__main__':
    teste = lexico("minicteste.c")
    teste.temporario()

