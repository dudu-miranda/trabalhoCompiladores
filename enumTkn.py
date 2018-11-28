#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Tabela de saida dos estados dos tokens
1-  print
2-  scan

3-  , (virgula)
4-  ; (ponto e virgula)
5-  ( (abre parentese)
6-  ) (fecha parentese)

7-  = (atribuicao)
8-  * (multiplicacao)
9-  + (adicao)
10- - (subtracao)
11- / (divisao)
12- % (modulo)

13- ||(or)
14- &&(and)
15- ! (not)
16- < (menor que)
17- > (maior que)
18- <=(menor ou igual)
19- >=(maior ou igual)
20- !=(desigualdade)
21- ==(igualdade)

22- int  (identificador de inteiros)
23- float (identificador de floats)

24- { (abre chaves)
25- } (fecha chaves)

26- break (saida de um laço)
27- continue (pulo de um laço)
28- for (inicio de loop)

29- scan (funcao para ler variavel)
30- print (funcao de saida de dados)

31- numInt (um numero inteiro)
32- numFloat (um numero float)

33- while (inicio do while)
34- var (palavra para condicao)
35- else (palavra para condicao)

36- EOF
"""


class enumTkn(object):
    tkn_in          = 1
    tkn_out         = 2
    tkn_virg        = 3
    tkn_ptVirg      = 4
    tkn_abrePar     = 5
    tkn_fechaPar    = 6
    tkn_atrib       = 7
    tkn_mult        = 8
    tkn_add         = 9
    tkn_sub         = 10
    tkn_div         = 11
    tkn_mod         = 12
    tkn_or          = 13
    tkn_and         = 14
    tkn_not         = 15
    tkn_menorQ      = 16
    tkn_maiorQ      = 17
    tkn_menorI      = 18
    tkn_maiorI      = 19
    tkn_diferenca   = 20
    tkn_igualdade   = 21
    tkn_int         = 22
    tkn_float       = 23
    tkn_abreCha     = 24
    tkn_fechaCha    = 25
    tkn_break       = 26
    tkn_continue    = 27
    tkn_for         = 28
    tkn_numInt      = 29
    tkn_numFloat    = 30
    tkn_while       = 31
    tkn_if          = 32
    tkn_else        = 33
    tkn_var         = 34
    tkn_str         = 35
    tkn_eof         = 36
    tkn_return		= 37