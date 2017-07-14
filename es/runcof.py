#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#    runcof.py
#    Programa para calcular el coeficiente de escurrimiento
#    usando la metodología de la norma mexicana NOM-011-CONAGUA-2015
#
#    Copyright 2012-2017 Eduardo Jimenez <ecoslacker@irriapps.com>
#
#    Permission is hereby granted, free of charge, to any person obtaining a
#    copy of this software and associated documentation files (the "Software"),
#    to deal in the Software without restriction, including without limitation
#    the rights to use, copy, modify, merge, publish, distribute, sublicense,
#    and/or sell copies of the Software, and to permit persons to whom the
#    Software is furnished to do so, subject to the following conditions:
#
#    The above copyright notice and this permission notice shall be included
#    in all copies or substantial portions of the Software.
#
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
#    THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#    DEALINGS IN THE SOFTWARE.

import argparse
from argparse import RawTextHelpFormatter

parser = argparse.ArgumentParser(
    description=u"Calcula el coeficiente de escurrimiento",
    formatter_class=RawTextHelpFormatter)
group = parser.add_mutually_exclusive_group()
group.add_argument("-v", "--verboso", action="store_true",
                   help=u"incrementa el modo verboso")
group.add_argument("-s", "--silencioso", action="store_true",
                   help=u"solo muestra el coeficiente de escurrimiento")
parser.add_argument("-a", "--area", type=float, nargs='+',
                    help=u"uno o más valores de área en hectareas o porcentaje")
parser.add_argument("-p", "--precipitacion", type=float,
                    help=u"precipitacion anual en milimetros")
parser.add_argument("-u", "--usosuelo", type=int, nargs='+',
                    choices=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
                    help=u"seleccionar uno o mas usos de suelo:\n"
                         u" 0 = Barbecho, areas incultas y desnudas\n"
                         u" 1 = Cultivos en hilera\n"
                         u" 2 = Legumbres o rotación de pradera\n"
                         u" 3 = Granos pequeños\n"
                         u" 4 = Pastizal (75%%)\n"
                         u" 5 = Pastizal (50-75%%)\n"
                         u" 6 = Pastizal (50%%)\n"
                         u" 7 = Bosque (75%%)\n"
                         u" 8 = Bosque (50-75%%)\n"
                         u" 9 = Bosque (25-50%%)\n"
                         u"10 = Bosque (25%%)\n"
                         u"11 = Zona urbana\n"
                         u"12 = Caminos\n"
                         u"13 = Pradera permanente\n")
parser.add_argument("-t", "--tiposuelo", type=int, choices=[0, 1, 2],
                    nargs='+', help=u"selecionar uno o mas tipos de suelo:\n"
                         u" 0 = Suelo permeable\n"
                         u" 1 = Suelo de permeabilidad media\n"
                         u" 2 = Suelo casi impermeable\n")
args = parser.parse_args()

usosuelo = [u"Barbecho, areas incultas y desnudas",
            u"Cultivos en hilera",
            u"Legumbres o rotación de pradera",
            u"Granos",
            u"Pastizal (75%%)",
            u"Pastizal (50-75%%)",
            u"Pastizal (50%%)",
            u"Bosque (75%%)",
            u"Bosque (50-75%%)",
            u"Bosque (25-50%%)",
            u"Bosque (25%%)",
            u"Zona urbana",
            u"Caminos",
            u"Pradera permanente"]
tiposuelo = [u"Suelo permeable",
             u"Suelo de permeabilidad media",
             u"Suelo casi impermeable"]
# A list of k values for each land use and soil type
k_list = [[0.26, 0.28, 0.30], [0.24, 0.27, 0.30], [0.24, 0.27, 0.30],
          [0.24, 0.27, 0.30], [0.14, 0.20, 0.28], [0.20, 0.24, 0.30],
          [0.24, 0.28, 0.30], [0.07, 0.16, 0.24], [0.12, 0.22, 0.26],
          [0.17, 0.26, 0.28], [0.22, 0.28, 0.30], [0.26, 0.29, 0.32],
          [0.27, 0.30, 0.33], [0.18, 0.24, 0.30]]
# Create a list with k values for each area
ka = []
area = 0.0
for i in range(len(args.area)):
    ka.append(k_list[args.usosuelo[i]][args.tiposuelo[i]])
    area += args.area[i]
# Sum all the values of (k * area)
k_sum = 0.0
for j in range(len(args.area)):
    # Get a partial value
    k_area = ka[j] * args.area[j]
    k_sum += k_area
# Get the mean of these values
k = k_sum / area
# And finally get the runoff coefficient
if k <= 0.15:
    coef_esc = k * (args.precipitacion - 250.0) / 2000.0
#elif k > 0.15:
else:
    coef_esc = k * (args.precipitacion - 250.0) / 2000.0 + (k - 0.15) / 1.5

# Print the outputs
if args.silencioso:
    print u"{0:.3f}".format(coef_esc)
elif args.verboso:
    for i in range(len(args.usosuelo)):
        print u"AREA - {}".format(i)
        print u"  Area: {0:.3f}".format(args.area[i])
        print u"  Uso de suelo: {}".format(usosuelo[args.usosuelo[i]])
        print u"  Tipo de suelo: {}".format(tiposuelo[args.tiposuelo[i]])
        print u"  Parametro K: {0:.3f}".format(ka[i])
        #print "  {0:.3f} * {0:.3f} = {0:.3f}".format(args.area[i], ka[i], args.area[i]*ka[i])
    print ""
    print u"Valor del area total: {0:.3f}".format(area)
    print u"Valor del parametro k: {0:.3f}".format(k)
    print u"Coeficiente de escurrimiento: {0:.3f}".format(coef_esc)
else:
    print ""
    for i in range(len(args.area)):
        print u"{0:.3f}".format(args.area[i])
        print u"{}".format(usosuelo[args.usosuelo[i]])
        print u"{}".format(tiposuelo[args.tiposuelo[i]])
        print u"{0:.3f}".format(ka[i])
        print ""
    print u"k: {0:.3f}".format(k)
    print u"Area: {0:.3f}".format(area)
    print u"Coeficiente de escurrimiento: {0:.3f}".format(coef_esc)
