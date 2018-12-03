#!/usr/bin/python
# -*- coding: utf-8 -*-
from trabalhoCompiladores.Error import ErroSintatico, ErroSemantico
from trabalhoCompiladores.sintatico import sintatico

try:
    sint=sintatico('prog1.c')
except ErroSintatico as e:
    print(e)

