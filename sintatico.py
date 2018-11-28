#!/usr/bin/python
# -*- coding: utf-8 -*-

from trabalhoCompiladores.lexico import *
from trabalhoCompiladores.enumTkn import enumTkn
from trabalhoCompiladores.Controle import Controle
from trabalhoCompiladores.Error import ErroSintatico, ErroSemantico


class sintatico(object):
    """docstring for sintatico"""
    def __init__(self,arquivo):
        super(sintatico, self).__init__()
        #Variavel com o nome do arquivo
        self.arquivo = arquivo
        #Analisador lexico
        self.l = lexico(arquivo)
        self.controle = Controle()
        self.function()


    #Função de iniciar o programa
    def function(self):
        self.consome(0)
        self.type()
        self.consome(enumTkn.tkn_var)
        self.consome(enumTkn.tkn_abrePar)
        self.argList()
        self.consome(enumTkn.tkn_fechaPar)
        self.bloco()


    def type(self):
        temp = self.l.token_atual
        if(self.l.token_atual==enumTkn.tkn_int):
            self.consome(enumTkn.tkn_int)
        else:
            self.consome(enumTkn.tkn_float)
        return temp

    def argList(self):
        if self.l.token_atual==enumTkn.tkn_int or self.l.token_atual==enumTkn.tkn_float:
            self.arg()
            self.restoArg()

    def arg(self):
        self.type()
        self.consome(enumTkn.tkn_var)

    def restoArg(self):
        if(self.l.token_atual==enumTkn.tkn_virg):
            self.argList()

    def bloco(self):
        self.consome(enumTkn.tkn_abreCha)
        self.stmtList()
        self.consome(enumTkn.tkn_fechaCha)

    def stmtList(self):
        lista = [enumTkn.tkn_not, enumTkn.tkn_abrePar, enumTkn.tkn_add, enumTkn.tkn_sub, enumTkn.tkn_ptVirg,
        enumTkn.tkn_var, enumTkn.tkn_float, enumTkn.tkn_int, enumTkn.tkn_break, enumTkn.tkn_continue, enumTkn.tkn_return,
        enumTkn.tkn_numFloat, enumTkn.tkn_numInt, enumTkn.tkn_for, enumTkn.tkn_if, enumTkn.tkn_in, enumTkn.tkn_out,
        enumTkn.tkn_while, enumTkn.tkn_abreCha]
        if(self.l.token_atual in lista):
            self.stmt()
            self.stmtList()

    def stmt(self):
        if(self.l.token_atual in [enumTkn.tkn_in, enumTkn.tkn_out]):
            self.ioStmt()

        elif(self.l.token_atual == enumTkn.tkn_for):
            self.forStmt()

        elif(self.l.token_atual == enumTkn.tkn_while):
            self.whileStmt()

        elif(self.l.token_atual in [enumTkn.tkn_not, enumTkn.tkn_abrePar, enumTkn.tkn_add, enumTkn.tkn_sub,
                                    enumTkn.tkn_var, enumTkn.tkn_numFloat, enumTkn.tkn_numInt]):
            self.expr()

        elif(self.l.token_atual == enumTkn.tkn_if):
            self.ifStmt()

        elif(self.l.token_atual == enumTkn.tkn_abreCha):
            self.bloco()

        elif(self.l.token_atual == enumTkn.tkn_break):
            self.consome(enumTkn.tkn_break)
            self.consome(enumTkn.tkn_ptVirg)

        elif(self.l.token_atual == enumTkn.tkn_continue):
            self.consome(enumTkn.tkn_continue)
            self.consome(enumTkn.tkn_ptVirg)

        elif(self.l.token_atual in [enumTkn.tkn_int, enumTkn.tkn_float]):
            self.declaration()

        elif(self.l.token_atual == enumTkn.tkn_return):
            self.consome(enumTkn.tkn_return)
            self.fator()
            self.consome(enumTkn.tkn_ptVirg)

        else:
            self.consome(enumTkn.tkn_ptVirg)

    def ioStmt(self):
        if self.l.token_atual == enumTkn.tkn_in:
            self.consome(enumTkn.tkn_in)
            self.consome(enumTkn.tkn_abrePar)
            self.outList()
            self.consome(enumTkn.tkn_fechaPar)
            self.consome(enumTkn.tkn_ptVirg)
        else:
            self.consome(enumTkn.tkn_out)
            self.consome(enumTkn.tkn_abrePar)
            self.consome(enumTkn.tkn_str)
            self.consome(enumTkn.tkn_virg)
            self.outList()
            self.consome(enumTkn.tkn_fechaPar)
            self.consome(enumTkn.tkn_ptVirg)

    def outList(self):
        self.out()
        self.restoOutList()

    def out(self):
        if self.l.token_atual == enumTkn.tkn_str: 
            self.consome(enumTkn.tkn_str)
        elif self.l.token_atual == enumTkn.tkn_numInt:
            self.consome(enumTkn.tkn_numInt)
        elif self.l.token_atual == enumTkn.tkn_numFloat:
            self.consome(enumTkn.tkn_numFloat)
        else:
            self.consome(enumTkn.tkn_var)

    def restoOutList(self):
        if self.l.token_atual == enumTkn.tkn_virg:
            self.consome(enumTkn.tkn_virg)
            self.out()
            self.restoOutList()

    def forStmt(self):
        self.consome(enumTkn.tkn_for)
        self.consome(enumTkn.tkn_abrePar)
        self.optexpr()
        self.consome(enumTkn.tkn_ptVirg)
        self.optexpr()
        self.consome(enumTkn.tkn_ptVirg)
        self.optexpr()
        self.consome(enumTkn.tkn_fechaPar)
        self.stmt()

    def optexpr(self):
        if self.l.token_atual in [enumTkn.tkn_not, enumTkn.tkn_abrePar, enumTkn.tkn_add, enumTkn.tkn_sub,
                                    enumTkn.tkn_var, enumTkn.tkn_numFloat, enumTkn.tkn_numInt]:
            self.expr()

    def whileStmt(self):
        self.consome(enumTkn.tkn_while)
        self.consome(enumTkn.tkn_abrePar)
        self.expr()
        self.consome(enumTkn.tkn_fechaPar)
        self.stmt()

    def expr(self):
        self.atrib()

    def atrib(self):
        a=self.functionOr()
        self.restoAtrib(a)

    def restoAtrib(self,bulian):
        if self.l.token_atual == enumTkn.tkn_atrib:
            if bulian:            
                self.consome(enumTkn.tkn_atrib)
                self.atrib()
            else:
                print('Erro de atribuicao na ' + 'l:'+str(self.l.linha)+' c:'+str(self.l.coluna))
                exit()

    def functionOr(self):
        a = self.functionAnd()
        b = self.restoOr()

        return a and b

    def restoOr(self):
        if self.l.token_atual == enumTkn.tkn_or:
            self.consome(enumTkn.tkn_or)
            self.functionAnd()
            self.restoOr()
        else:
            return True

        return False

    def functionAnd(self):
        a=self.functionNot()
        b=self.restoAnd()

        return a and b

    def restoAnd(self):
        if self.l.token_atual == enumTkn.tkn_and:
            self.consome(enumTkn.tkn_and)
            self.functionNot()
            self.restoAnd()
        else:
            return True

        return False

    def functionNot(self):
        if self.l.token_atual == enumTkn.tkn_not:
            self.consome(enumTkn.tkn_not)
            self.functionNot()
        else:
            return self.rel()

        return False

    def rel(self):
        a=self.add()
        b=self.restorel()

        return a and b

    def restorel(self):
        if self.l.token_atual == enumTkn.tkn_igualdade:
            self.consome(enumTkn.tkn_igualdade)
            self.add()
        elif self.l.token_atual == enumTkn.tkn_diferenca:
            self.consome(enumTkn.tkn_diferenca)
            self.add()
        elif self.l.token_atual == enumTkn.tkn_menorQ:
            self.consome(enumTkn.tkn_menorQ)
            self.add()
        elif self.l.token_atual == enumTkn.tkn_maiorQ:
            self.consome(enumTkn.tkn_maiorQ)
            self.add()
        elif self.l.token_atual == enumTkn.tkn_maiorI:
            self.consome(enumTkn.tkn_maiorI)
            self.add()
        elif self.l.token_atual == enumTkn.tkn_menorI:
            self.consome(enumTkn.tkn_menorI)
            self.add()
        else:
            return True

        return False

    def add(self):
        a = self.mult()
        b = self.restoAdd()

        return a and b

    def restoAdd(self):
        if self.l.token_atual == enumTkn.tkn_add:
            self.consome(enumTkn.tkn_add)
            self.mult()
            self.restoAdd()
        elif self.l.token_atual == enumTkn.tkn_sub:
            self.consome(enumTkn.tkn_sub)
            self.mult()
            self.restoAdd()
        else:
            return True

        return False    

    def mult(self):
        a=self.uno()
        b=self.restoMult()

        return a and b

    def restoMult(self):
        if self.l.token_atual == enumTkn.tkn_mult:
            self.consome(enumTkn.tkn_mult)
            self.uno()
            self.restoMult()
        elif self.l.token_atual == enumTkn.tkn_div:
            self.consome(enumTkn.tkn_div)
            self.uno()
            self.restoMult()
        elif self.l.token_atual == enumTkn.tkn_mod:
            self.consome(enumTkn.tkn_mod)
            self.uno()
            self.restoMult()
        else:
            return True

        return False

    def uno(self):
        if self.l.token_atual == enumTkn.tkn_add:
            self.consome(enumTkn.tkn_add)
            (left, lista, res) = self.uno()
            novotemp = self.controle.geraTemp() # geratemporario
            quad = ("+", novotemp, 0, res)
            novalista = lista + quad
            return (False, novalista, novotemp)
        elif self.l.token_atual == enumTkn.tkn_sub:
            self.consome(enumTkn.tkn_sub)
            (left, lista, res) = self.uno()
            novotemp = self.controle.geraTemp()  # geratemporario
            quad = ("-", novotemp, 0, res)
            novalista = lista + quad
            return (False, novalista, novotemp)
        else:
            return self.fator()

    
    # (left, # lista de comandos, resultado dos comandos)

    def fator(self):
        if self.l.token_atual == enumTkn.tkn_numFloat:
            self.consome(enumTkn.tkn_numFloat)
            return (False, [], self.l.lexema)
        elif self.l.token_atual == enumTkn.tkn_var:
            self.consome(enumTkn.tkn_var)
            return (True, [], self.l.lexema)
        elif self.l.token_atual == enumTkn.tkn_abrePar:
            self.consome(enumTkn.tkn_abrePar)
            (left, lista, res) = self.atrib()
            self.consome(enumTkn.tkn_fechaPar)
            return (False, lista, res)
        else:
            self.consome(enumTkn.tkn_numInt)
            return (False, [], self.l.lexema)

    def ifStmt(self):
        self.consome(enumTkn.tkn_if)
        self.consome(enumTkn.tkn_abrePar)
        self.expr()
        self.consome(enumTkn.tkn_fechaPar)
        self.stmt()
        self.elsepart()

    def elsepart(self):
        if self.l.token_atual == enumTkn.tkn_else:
            self.consome(enumTkn.tkn_else)
            self.stmt()

    def declaration(self):
        temp1 = self.type()
        temp2 = self.identList()
        for variavel in temp2:
            self.controle.add_simbolo(variavel,temp1)
        self.consome(enumTkn.tkn_ptVirg)

    def identList(self):
        #Guarda o primeiro identificador
        lista = [self.l.token_atual]
        #Consome uma variavel
        self.consome(enumTkn.tkn_var)
        #Da um extend na lista que sera recebido da recursão
        lista.extend(self.restoidentList())
        #Retorna a lista 
        return lista

    def restoidentList(self):
        lista = []
        #Caso tenha mais um token
        if self.l.token_atual == enumTkn.tkn_virg :
            #Consome a virgula
            self.consome(enumTkn.tkn_virg)
            #Da um append na lista atual com o token atual
            lista.append(self.l.token_atual)
            #Consome um token IDENT
            self.consome(enumTkn.tkn_var)
            #Da um extend da proxima recursão da lista que retornará outra lista nem que seja vazia
            lista.extend(self.restoidentList())

        return lista

    def consome(self, token):

        if token == self.l.token_atual or token==0:
            self.l.getToken()
            return 0

        lista=['','print','scan',',',';','(',')','=','*','+','-','/','%','||','&&','!',
                '<','>','<=','>=','!=','==','int','float','{','}','break','continue','for',
                'numero','numero','while','if','else','identificador','string','eof','return']

        msg = ('Era esperado o token ' + lista[token] + ', foi recebido ' + str(self.l.lexema))
        raise ErroSintatico((self.l.linha, self.l.coluna), msg)
