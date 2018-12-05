#!/usr/bin/python
# -*- coding: utf-8 -*-
from trabalhoCompiladores.sintatico import sintatico
from trabalhoCompiladores.maquinaVirtual import maquinaVirtual


sint=sintatico('prog1.c')

prog = sint.solve()

maquina = maquinaVirtual(prog)
maquina.ligar()
