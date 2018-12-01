# -*- coding: utf-8 -*-


class Error(Exception):
    pass


class ErroSintatico(Error):

    """
    Exceções levantadas por error sintaticos
    tpl -- tupla com linha e coluna onde ocorreu o erro
    msg -- explicação do erro
    """
    def __init__(self, tpl, msg):
        self.tpl = tpl
        self.msg = msg

    def __str__(self):
        vermelho = '\033[31m'
        original = '\033[0;0m'
        amarelo = '\033[33m'
        erro = vermelho + "Erro Sintatico:"
        erro += original + " linha %d coluna %d" %(self.tpl[0], self.tpl[1])
        erro += '\n'
        erro += self.msg
        return erro


class ErroSemantico(Error):
    """
    Exceções levantadas por error semanticos
    tpl -- tupla com linha e coluna onde ocorreu o erro
    msg -- explicação do erro
    """
    def __init__(self, tpl, msg):
        self.tpl = tpl
        self.msg = msg

    def __str__(self):
        vermelho = '\033[31m'
        original = '\033[0;0m'
        erro = vermelho + "Erro Semantico: "
        erro += original + "linha %d coluna %d" %(self.tpl[0], self.tpl[1])
        erro += '\n'
        erro += self.msg
        return erro
