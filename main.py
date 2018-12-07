#!/usr/bin/python
# -*- coding: utf-8 -*-
from trabalhoCompiladores.sintatico import sintatico
from trabalhoCompiladores.maquinaVirtual import maquinaVirtual


sint=sintatico('pExpressoesBasicas.c')
#sint=sintatico('pBlocos.c')
#sint=sintatico('pBlocos.c')
#sint=sintatico('pBlocos.c')

#sint=sintatico('prog1.c')
#sint=sintatico('prog2.c')
#sint=sintatico('prog3.c')

prog = sint.solve()

maquina = maquinaVirtual(prog)
maquina.ligar()
