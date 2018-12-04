#!/usr/bin/python
# -*- coding: utf-8 -*-
from trabalhoCompiladores.Error import ErroSintatico, ErroSemantico
from trabalhoCompiladores.sintatico import sintatico
from trabalhoCompiladores.maquinaVirtual import maquinaVirtual

sint = None
try:
    sint=sintatico('prog1.c')
except ErroSintatico as e:
    print(e)
