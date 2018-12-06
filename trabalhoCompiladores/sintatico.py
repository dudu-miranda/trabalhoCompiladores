#!/usr/bin/python
# -*- coding: utf-8 -*-

from trabalhoCompiladores.lexico import *
from trabalhoCompiladores.enumTkn import enumTkn
from trabalhoCompiladores.Controle import Controle
from trabalhoCompiladores.Error import ErroSintatico


class sintatico(object):
    """docstring for sintatico"""
    def __init__(self,arquivo):
        #Variavel com o nome do arquivo
        self.arquivo = arquivo
        #Analisador lexico
        self.l = lexico(arquivo)
        self.controle = Controle()
        self.__listaBLoco = []
        # self.meucaminhobloco = []    # pilha ate o bloco atual

    def solve(self):
        try:
            return self.function()
        except ErroSintatico as e:
            exit(e)

    #Função de iniciar o programa
    def function(self):
        """
        # <function*> -> <type> 'IDENT' '(' <argList> ')' <bloco> ;
        :return:
        """

        arq = open('saida.txt', "w")

        meubloco = self.controle.gerabloco()
        self.__listaBLoco.append(meubloco)

        lista_comandos = []
        self.consome(0)
        tipo = self.type()
        self.consome(enumTkn.tkn_var)
        self.consome(enumTkn.tkn_abrePar)

        lista_comandos.extend(self.argList())
        self.consome(enumTkn.tkn_fechaPar)
        
        lista_comandos.extend(self.bloco())

        arq.write(str(lista_comandos))

        self.__listaBLoco.remove(meubloco)
        return lista_comandos

    def type(self):
        """
        Verifica o tipo do token
        :return: token
        """

        tipo = self.l.token_atual
        if self.l.token_atual == enumTkn.tkn_int:
            self.consome(enumTkn.tkn_int)
        else:
            self.consome(enumTkn.tkn_float)
        return tipo

    def argList(self):
        """
        # <argList> -> <arg> <restoArgList> | & ;
        :return:
        """
        lista_arg = []
        if self.l.token_atual == enumTkn.tkn_int or self.l.token_atual == enumTkn.tkn_float:
            lista_arg.append(self.arg())
            lista_arg.extend(self.restoArg())

        return lista_arg

    def arg(self):
        """
        # <arg> -> <type> 'IDENT' ;
        :return:
        """

        tipo = self.type()
        variavel = self.l.lexema
        self.consome(enumTkn.tkn_var)
        if not self.controle.add_simbolo(variavel, tipo):
            msg = "Variavel redeclarada"
            raise ErroSintatico((self.l.linha, self.l.coluna), msg)

        if tipo == enumTkn.tkn_int:
            atrib = ('=', variavel, 0, None)
        else:
            atrib = ('=', variavel, 0.0, None)

        return atrib

    def restoArg(self):
        """
            <restoArgList> -> ',' <argList> | & ;
        """
        lista_arg = []

        if self.l.token_atual == enumTkn.tkn_virg:
            self.consome(enumTkn.tkn_virg)
            lista_arg = self.argList()

        return lista_arg

    def bloco(self, labelContinue = None, labelBreak = None):
        """
        <bloco> -> '{' <stmtList> '}' ;
        :return:
        """
        # definindo em qual bloco estou


        lista = []
        self.consome(enumTkn.tkn_abreCha)
        lista.extend(self.stmtList(labelContinue, labelBreak))
        self.consome(enumTkn.tkn_fechaCha)

        # saindo do bloco


        return lista

    def stmtList(self, labelContinue = None, labelBreak = None):
        """
        <stmtList> -> <stmt> <stmtList> | <declaration> | & ;
        :return:
        """
        listaDeBlocos = []

        lista = [enumTkn.tkn_not, enumTkn.tkn_abrePar, enumTkn.tkn_add, enumTkn.tkn_sub, enumTkn.tkn_ptVirg,
        enumTkn.tkn_var, enumTkn.tkn_float, enumTkn.tkn_int, enumTkn.tkn_break, enumTkn.tkn_continue, enumTkn.tkn_return,
        enumTkn.tkn_numFloat, enumTkn.tkn_numInt, enumTkn.tkn_for, enumTkn.tkn_if, enumTkn.tkn_in, enumTkn.tkn_out,
        enumTkn.tkn_while, enumTkn.tkn_abreCha]

        if self.l.token_atual in [enumTkn.tkn_int, enumTkn.tkn_float]:
            listaDeBlocos.extend(self.declaration())
            listaDeBlocos.extend(self.stmtList(labelContinue,labelBreak))

        elif self.l.token_atual in lista:
            listaDeBlocos.extend(self.stmt(labelContinue,labelBreak))
            listaDeBlocos.extend(self.stmtList(labelContinue,labelBreak))

        return listaDeBlocos

    def stmt(self, labelContinue = None, labelBreak=None):
        """
        <stmt> -> <forStmt> | <ioStmt> | <whileStmt> | <expr> ';' | <ifStmt> | <bloco> | 'break' | 'continue' | ';' ;

        :return:
        """
        
        lista = []
        if self.l.token_atual in [enumTkn.tkn_in, enumTkn.tkn_out]:
            lista.extend(self.ioStmt())

        elif self.l.token_atual == enumTkn.tkn_for:
            lista.extend(self.forStmt())

        elif self.l.token_atual == enumTkn.tkn_while:
            lista.extend(self.whileStmt())

        elif(self.l.token_atual in [enumTkn.tkn_not, enumTkn.tkn_abrePar, enumTkn.tkn_add, enumTkn.tkn_sub,
                                    enumTkn.tkn_var, enumTkn.tkn_numFloat, enumTkn.tkn_numInt]):
            lst, var = self.expr()
            lista.extend(lst)
            self.consome(enumTkn.tkn_ptVirg)

        elif self.l.token_atual == enumTkn.tkn_if:
            lista.extend(self.ifStmt())

        elif self.l.token_atual == enumTkn.tkn_abreCha:
            meubloco = self.controle.gerabloco()
            self.__listaBLoco.append(meubloco)
            lista.extend(self.bloco(labelContinue, labelBreak))
            self.__listaBLoco.remove(meubloco)

        elif self.l.token_atual == enumTkn.tkn_break:
            self.consome(enumTkn.tkn_break)

            lista.append(('JUMP', labelBreak, None, None))

        elif self.l.token_atual == enumTkn.tkn_continue:
            self.consome(enumTkn.tkn_continue)

            lista.append(('JUMP', labelContinue, None, None))

        elif self.l.token_atual == enumTkn.tkn_return:
            self.consome(enumTkn.tkn_return)
            self.fator()
            lista.append(('CALL', 'STOP', None, None))
            self.consome(enumTkn.tkn_ptVirg)

        else:
            self.consome(enumTkn.tkn_ptVirg)

        
        return lista

    def ioStmt(self):
        """
        <ioStmt> -> 'scan' '(' 'IDENT' ')' ';'  | 'print' '(' <outList> ')' ';' ;
        :return:
        """

        listaCmd = []

        if self.l.token_atual == enumTkn.tkn_in:
            self.consome(enumTkn.tkn_in)
            self.consome(enumTkn.tkn_abrePar)
            string = self.l.lexema
            listaCmd.append(('CALL', 'PRINT', string, None))
            self.consome(enumTkn.tkn_str)
            self.consome(enumTkn.tkn_virg)
            
            variavelEntrada = self.l.lexema
            verifica = self.controle.verifica_simbolo(variavelEntrada, self.__listaBLoco)

            if not verifica:
                msg = "Variavel %s não foi declarada." % variavelEntrada
                raise ErroSintatico((self.l.linha, self.l.coluna), msg)

            listaCmd.append(('CALL', 'SCAN', None, variavelEntrada+verifica))
            self.consome(enumTkn.tkn_var)
            self.consome(enumTkn.tkn_fechaPar)
            self.consome(enumTkn.tkn_ptVirg)
        else:
            self.consome(enumTkn.tkn_out)
            self.consome(enumTkn.tkn_abrePar)
            listaCmd.extend(self.outList())
            self.consome(enumTkn.tkn_fechaPar)
            self.consome(enumTkn.tkn_ptVirg)

        return listaCmd

    def outList(self):
        """
        <outList> -> <out> <restoOutList> ;   
        :return:
        """

        listaSaida = []
        listaSaida.append(self.out())
        listaSaida.extend(self.restoOutList())

        return listaSaida

    def out(self):
        """
        <out> -> 'STR' | 'IDENT' | 'NUMint' | 'NUMfloat' ;
        :return:
        """
        coisaPraPrintar = self.l.lexema
        if self.l.token_atual == enumTkn.tkn_str: 
            self.consome(enumTkn.tkn_str)
        elif self.l.token_atual == enumTkn.tkn_numInt:
            self.consome(enumTkn.tkn_numInt)
        elif self.l.token_atual == enumTkn.tkn_numFloat:
            self.consome(enumTkn.tkn_numFloat)
        else:
            self.consome(enumTkn.tkn_var)
            verifica = self.controle.verifica_simbolo(coisaPraPrintar, self.__listaBLoco)
            if not verifica:
                msg = "Variavel %s não foi declarada." % coisaPraPrintar
                raise ErroSintatico((self.l.linha, self.l.coluna), msg)
            
            return ('CALL','PRINT',None,coisaPraPrintar + verifica)

        return ('CALL', 'PRINT', coisaPraPrintar, None)

    def restoOutList(self):
        """
        <restoOutList> -> ',' <out> <restoOutList> | & ;
        :return:
        """
        lista = []
        if self.l.token_atual == enumTkn.tkn_virg:
            self.consome(enumTkn.tkn_virg)
            lista.append(self.out())
            lista.extend(self.restoOutList())

        return lista

    def forStmt(self):
        """
        <forStmt> -> 'for' '(' <optExpr> ';' <optExpr> ';' <optExpr> ')' <stmt> ;
        :return:
        """

        lista = []
        labelexp = self.controle.geraLabel()
        labelinicio = self.controle.geraLabel()
        labelfim = self.controle.geraLabel()

        self.consome(enumTkn.tkn_for)
        self.consome(enumTkn.tkn_abrePar)
        listaopr, variavelR = self.optexpr()
        lista.extend(listaopr)

        self.consome(enumTkn.tkn_ptVirg)
        
        # calculo da expressao
        lista.append(('LABEL', labelexp, None, None))
        listaopr, variavelR = self.optexpr()
        lista.extend(listaopr) # calculo de fato adicionado ao comando
        if(variavelR != None):
            lista.append(("IF", variavelR, labelinicio, labelfim))
        
        self.consome(enumTkn.tkn_ptVirg)

        # a operacao e feita ao final do stmt
        listaINC, variavelR = self.optexpr()
        self.consome(enumTkn.tkn_fechaPar)

        lista.append(('LABEL', labelinicio, None, None))
        lista.extend(self.stmt())

        lista.extend(listaINC)     # adicionando o calculo do incremento

        lista.append(('JUMP', labelexp, None, None))    # volta verificacao
        lista.append(('LABEL', labelfim, None, None))   # label de final
        return lista

    def optexpr(self):
        """
        <optExpr> -> <expr> | & ;
        :return:
        """
        listaopr = []
        variavelresult = None
        if self.l.token_atual in [enumTkn.tkn_not, enumTkn.tkn_abrePar, enumTkn.tkn_add, enumTkn.tkn_sub,
                                    enumTkn.tkn_var, enumTkn.tkn_numFloat, enumTkn.tkn_numInt]:
            listaopr, variavelresult = self.expr()

        return listaopr, variavelresult

    def whileStmt(self):
        self.consome(enumTkn.tkn_while)
        self.consome(enumTkn.tkn_abrePar)

        labelExpressao = self.controle.geraLabel()
        labelAposExpressao = self.controle.geraLabel()
        labelSaida = self.controle.geraLabel()

        lista = []
        #Coloca o label do calculo da expressao
        lista.append(('LABEL',labelExpressao,None,None))

        #Pega o codigo que calcula a expressao de saida do while pela primeira vez
        listaExpressao, res = self.expr()
        lista.extend(listaExpressao)
        
        #Faz um if pra primeira vez que caso a expressao seja falsa ele vai para a saida caso contrario ele continua no codigo do bloco
        lista.append(("IF", res, labelAposExpressao,labelSaida))
        #Coloca o label do pos expressao
        lista.append(('LABEL', labelAposExpressao,None,None))

        self.consome(enumTkn.tkn_fechaPar)

        #Chama um stmt passando os labels de saida e de expressao para caso seja um break ou continue
        lista.extend(self.stmt(labelExpressao, labelSaida))

        #Manda lá pra cima para ser calculada a expressao novamente para decidir se vai ou nao sair do laço
        lista.append(('JUMP', labelExpressao, None, None))

        #Adiciona o label de saida do laço
        lista.append(('LABEL', labelSaida, None, None))

        return lista

    def expr(self):
        """
        <expr> -> <atrib> ;
        :return:
        """
        left, listaComandos, resultado = self.atrib()
        if listaComandos is None:
            listaComandos = []

        return listaComandos, resultado

    def atrib(self):
        """
        <atrib> -> <or> <restoAtrib> ;
        :return:
        """
        leftValue, listaComandos, resultado = self.functionOr()
        leftValueb, listaComandosb, resultadob = self.restoAtrib(leftValue)
        if resultadob is not None:
            listaComandos.extend(listaComandosb)
            listaComandos.append(('=', resultado, resultadob, None))

        return leftValue and leftValueb, listaComandos, resultado

    def restoAtrib(self, bulian):
        """
        <restoAtrib> -> '=' <atrib> | & ;
        :param bulian:
        :return:
        """
        if self.l.token_atual == enumTkn.tkn_atrib:
            if bulian:            
                self.consome(enumTkn.tkn_atrib)
                return self.atrib()
            else:
                msg = "Não é possivel realizar esta operação de atribuição."
                raise ErroSintatico((self.l.linha, self.l.coluna), msg)
        else:
            return bulian, [], None

    def functionOr(self):
        """
        <or> -> <and> <restoOr> ;
        :return:
        """
        leftValue, listaComandos, resultado = self.functionAnd()
        leftValueb, listaComandosb, resultadob = self.restoOr(resultado)
        listaComandos.extend(listaComandosb)
        return leftValue and leftValueb, listaComandos, resultadob

    def restoOr(self, resultant):
        """
        <restoOr> -> '||' <and> <restoOr> | & ;
        :return:
        """
        if self.l.token_atual == enumTkn.tkn_or:
            opr = self.l.lexema
            self.consome(enumTkn.tkn_or)
            leftValue, listaComandos, resultado = self.functionAnd()

            novotemp = self.controle.geraTemp() # ficara o resultado do or

            listaComandos.append((opr, novotemp, resultado, resultant))
            leftValueb, listaComandosb, resultadob = self.restoOr(novotemp)
            listaComandos.extend(listaComandosb)

            return False, listaComandos, resultadob
        else:
            return True, [], resultant

    def functionAnd(self):
        leftValue, listaComandos, resultado = self.functionNot()
        leftValueb, listaComandosb, resultadob = self.restoAnd(resultado)
        listaComandos.extend(listaComandosb)
        return leftValue and leftValueb, listaComandos, resultadob

    def restoAnd(self, resultant):
        """
        <restoAnd> -> '&&' <not> <restoAnd> | & ;
        :param resultant:
        :return:
        """
        if self.l.token_atual == enumTkn.tkn_and:
            opr = self.l.lexema
            self.consome(enumTkn.tkn_and)
            leftValue, listaComandos, resultado = self.functionNot()

            novotemp = self.controle.geraTemp()  # ficara o resultado do amd
            listaComandos.append((opr, novotemp, resultant, resultado))

            leftValueb, listaComandosb, resultadob = self.restoAnd(novotemp)
            listaComandos.extend(listaComandosb)

            return False, listaComandos, resultadob
        else:
            return True, [], resultant

    def functionNot(self):
        """
        <not> -> '!' <not> | <rel> ;
        :return:
        """

        if self.l.token_atual == enumTkn.tkn_not:
            opr = self.l.lexema
            self.consome(enumTkn.tkn_not)
            leftValue, listaComandos, resultado = self.functionNot()
            novotemp = self.controle.geraTemp()
            listaComandos.append((opr, novotemp, resultado, None))
            return False, listaComandos, novotemp
        else:
            return self.rel()

    def rel(self):
        """
        <rel> -> <add> <restoRel> ;
        :return:
        """
        leftValue, listaComandos, resultado = self.add()
        leftValueb, listaComandosb, resultadob = self.restorel(resultado)
        listaComandos.extend(listaComandosb)
        return leftValue and leftValueb, listaComandos, resultadob

    def restorel(self, resultadoAnt):
        """
        <restoRel> -> '==' <add> | '!=' <add>
            | '<' <add> | '<=' <add>
            | '>' <add> | '>=' <add> | & ;
        :param resultado: resultado da operacao anterior
        :return:
        """
        comparacao = self.l.lexema
        if self.l.token_atual == enumTkn.tkn_igualdade:
            self.consome(enumTkn.tkn_igualdade)
            leftValue, listaComandos, resultado = self.add()
        elif self.l.token_atual == enumTkn.tkn_diferenca:
            self.consome(enumTkn.tkn_diferenca)
            leftValue, listaComandos, resultado = self.add()
        elif self.l.token_atual == enumTkn.tkn_menorQ:
            self.consome(enumTkn.tkn_menorQ)
            leftValue, listaComandos, resultado = self.add()
        elif self.l.token_atual == enumTkn.tkn_maiorQ:
            self.consome(enumTkn.tkn_maiorQ)
            leftValue, listaComandos, resultado = self.add()
        elif self.l.token_atual == enumTkn.tkn_maiorI:
            self.consome(enumTkn.tkn_maiorI)
            leftValue, listaComandos, resultado = self.add()
        elif self.l.token_atual == enumTkn.tkn_menorI:
            self.consome(enumTkn.tkn_menorI)
            leftValue, listaComandos, resultado = self.add()
        else:
            return True, [], resultadoAnt  # retorna o propio resultado anterior

        novotemp = self.controle.geraTemp()   # guardara o resultado da operacao
        listaComandos.append((comparacao, novotemp, resultadoAnt, resultado))
        return False, listaComandos, novotemp

    def add(self):
        """
        <add> -> <mult> <restoAdd> ;
        :return:
        """
        leftValue, listaComandos, resultado = self.mult()
        leftValueb, listaComandosb, resultadob = self.restoAdd(resultado)
        listaComandos.extend(listaComandosb)
        return leftValue and leftValueb, listaComandos, resultadob


    # falta so daqui pra baixo
    def restoAdd(self, resultant):
        """
        <restoAdd> -> '+' <mult> <restoAdd>
            | '-' <mult> <restoAdd> | & ;
        :param resultant:
        :return:
        """
        if self.l.token_atual == enumTkn.tkn_add:
            opr = self.l.lexema
            self.consome(enumTkn.tkn_add)
            leftValue, listaComandos, resultado = self.mult()
            novotemp = self.controle.geraTemp()
            listaComandos.append((opr, novotemp, resultant, resultado))
            leftValueb, listaComandosb, resultadob = self.restoAdd(novotemp)
            listaComandos.extend(listaComandosb)

            return False, listaComandos, resultadob

        elif self.l.token_atual == enumTkn.tkn_sub:
            opr = self.l.lexema
            self.consome(enumTkn.tkn_sub)
            leftValue, listaComandos, resultado = self.mult()
            novotemp = self.controle.geraTemp()
            listaComandos.append((opr, novotemp, resultant, resultado))
            leftValueb, listaComandosb, resultadob = self.restoAdd(novotemp)
            listaComandos.extend(listaComandosb)

            return False, listaComandos, resultadob
        else:
            return True, [], resultant

    def mult(self):
        leftValue, listaComandos, resultado = self.uno()
        leftValueb, listaComandosb, resultadob = self.restoMult(resultado)
        listaComandos.extend(listaComandosb)
        return leftValue and leftValueb, listaComandos, resultadob

    def restoMult(self, resultadoant):
        opr = self.l.lexema
        if self.l.token_atual == enumTkn.tkn_mult:
            self.consome(enumTkn.tkn_mult)
            leftValue, listaComandos, resultado = self.uno()
            novoTemp = self.controle.geraTemp()
            listaComandos.append((opr, novoTemp, resultadoant, resultado))
            leftValueb, listaComandosb, resultadob = self.restoMult(novoTemp)

            listaComandos.extend(listaComandosb)

        elif self.l.token_atual == enumTkn.tkn_div:
            self.consome(enumTkn.tkn_div)
            leftValue, listaComandos, resultado = self.uno()
            novoTemp = self.controle.geraTemp()
            listaComandos.append((opr, novoTemp, resultadoant, resultado))
            leftValueb, listaComandosb, resultadob = self.restoMult(novoTemp)
            listaComandos.extend(listaComandosb)

        elif self.l.token_atual == enumTkn.tkn_mod:
            self.consome(enumTkn.tkn_mod)
            leftValue, listaComandos, resultado = self.uno()
            novoTemp = self.controle.geraTemp()
            listaComandos.append((opr, novoTemp, resultadoant, resultado))
            leftValueb, listaComandosb, resultadob = self.restoMult(novoTemp)
            listaComandos.extend(listaComandosb)
        else:
            return True, [], resultadoant

        return False, listaComandos, resultadob

    def uno(self):
        if self.l.token_atual == enumTkn.tkn_add:
            self.consome(enumTkn.tkn_add)
            (left, lista, res) = self.uno()
            novotemp = self.controle.geraTemp() # geratemporario
            quad = ("+", novotemp, 0, res)
            novalista = lista + [quad]
            return (False, novalista, novotemp)

        elif self.l.token_atual == enumTkn.tkn_sub:
            self.consome(enumTkn.tkn_sub)
            (left, lista, res) = self.uno()
            novotemp = self.controle.geraTemp()  # geratemporario
            quad = ("-", novotemp, 0, res)
            novalista = lista + [quad]
            return (False, novalista, novotemp)
        else:
            return self.fator()

    
    # (left, # lista de comandos, resultado dos comandos)

    def fator(self):
        atual = self.l.lexema
        if self.l.token_atual == enumTkn.tkn_numFloat:
            self.consome(enumTkn.tkn_numFloat)
            return (False, [], atual)
        elif self.l.token_atual == enumTkn.tkn_var:
            verifica = self.controle.verifica_simbolo(atual, self.__listaBLoco)
            if not verifica:
                msg = "Variavel %s não foi declarada." % atual
                raise ErroSintatico((self.l.linha, self.l.coluna), msg)
            self.consome(enumTkn.tkn_var)
            return (True, [], atual+verifica)

        elif self.l.token_atual == enumTkn.tkn_abrePar:
            self.consome(enumTkn.tkn_abrePar)
            left, lista, res = self.atrib()
            self.consome(enumTkn.tkn_fechaPar)
            return (False, lista, res)

        else:
            self.consome(enumTkn.tkn_numInt)
            return (False, [], atual)

    def ifStmt(self):

        lista = []

        self.consome(enumTkn.tkn_if)
        self.consome(enumTkn.tkn_abrePar)
        
        lstExpr, result = self.expr()
        
        self.consome(enumTkn.tkn_fechaPar)

        vdd = self.controle.geraLabel()
        labelAposExpressao = self.controle.geraLabel()
        falsidade = self.controle.geraLabel()

        blocoIF = self.stmt()
        blocoElse = self.elsepart()

        lista.extend(lstExpr)
        lista.append(("IF",result,labelAposExpressao,falsidade))
        lista.append(("LABEL",labelAposExpressao,None,None))
        lista.extend(blocoIF)
        lista.append(("JUMP",vdd,None,None))
        lista.append(("LABEL",falsidade,None,None))
        lista.extend(blocoElse)
        lista.append(("LABEL",vdd,None,None))

        return lista

    def elsepart(self):
        lista = []
        if self.l.token_atual == enumTkn.tkn_else:
            self.consome(enumTkn.tkn_else)
            lista.extend(self.stmt())

        return lista

    def declaration(self):
        tipo = self.type()
        temp2 = self.identList()
        lista = []

        for variavel in temp2:

            if not self.controle.add_simbolo(variavel, tipo, self.__listaBLoco[-1]):
                msg = "Variavel "+variavel+" redeclarada"
                raise ErroSintatico((self.l.linha, self.l.coluna), msg)
            if tipo == enumTkn.tkn_int:
                atrib = ('=', variavel + self.__listaBLoco[-1], 0, None)
            else:
                atrib = ('=', variavel + self.__listaBLoco[-1], 0.0, None)

            lista.append(atrib)

        self.consome(enumTkn.tkn_ptVirg)

        return lista

    def identList(self):
        #Guarda o primeiro identificador
        lista = [self.l.lexema]
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
            #Da um append na lista atual com o nome da variavel atual
            lista.append(self.l.lexema)
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
