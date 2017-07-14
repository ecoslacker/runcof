#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#    runcof.py
#    Command line program/script to calculate the runoff coefficient,
#    using the NOM-011-CNA-2000 methodology from Mexico
#
#    Copyright 2012 Eduardo Jimenez <ecoslacker@irriapps.org>
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
    description="Get the runoff coefficient",
    formatter_class=RawTextHelpFormatter)
group = parser.add_mutually_exclusive_group()
group.add_argument("-v", "--verbose", action="store_true",
                   help="increase output verbosity")
group.add_argument("-q", "--quiet", action="store_true",
                   help="just show the runoff coefficient")
parser.add_argument("-a", "--area", type=float, nargs='+',
                    help="one or more area values in hectares or percent")
parser.add_argument("-p", "--precipitation", type=float,
                    help="the value of anual precipitation in milimeters")
parser.add_argument("-l", "--landuse", type=int, nargs='+',
                    choices=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
                    help="select one or more land uses where:\n"
                         " 0 = Fallow or bare ground\n"
                         " 1 = Row crops\n"
                         " 2 = Vegetables or grassland rotation\n"
                         " 3 = Small grain crops\n"
                         " 4 = Pastureland (75%%)\n"
                         " 5 = Pastureland (50-75%%)\n"
                         " 6 = Pastureland (50%%)\n"
                         " 7 = Forest (75%%)\n"
                         " 8 = Forest (50-75%%)\n"
                         " 9 = Forest (25-50%%)\n"
                         "10 = Forest (25%%)\n"
                         "11 = Urban\n"
                         "12 = Roads\n"
                         "13 = Grassland\n")
parser.add_argument("-s", "--soiltype", type=int, choices=[0, 1, 2],
                    nargs='+', help="select one or more soil types where:\n"
                         " 0 = Permeable soil\n"
                         " 1 = Medium permeability\n"
                         " 2 = Almost impermeable\n")
args = parser.parse_args()

landuse = ["Fallow or bare ground",
           "Row crops",
           "Vegetables or grassland rotation",
           "Small grain crops",
           "Pastureland (75%)",
           "Pastureland (50-75%)",
           "Pastureland (50%)",
           "Forest (75%)",
           "Forest (50-75%)",
           "Forest (25-50%)",
           "Forest (25%)",
           "Urban",
           "Roads",
           "Grassland"]
soiltype = ["Permeable soil",
            "Medium permeability",
            "Almost impermeable"]
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
    ka.append(k_list[args.landuse[i]][args.soiltype[i]])
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
    runoff_coef = k * (args.precipitation - 250.0) / 2000.0
#elif k > 0.15:
else:
    runoff_coef = k * (args.precipitation - 250.0) / 2000.0 + (k - 0.15) / 1.5

# Print the outputs
if args.quiet:
    print "{0:.3f}".format(runoff_coef)
elif args.verbose:
    for i in range(len(args.landuse)):
        print "AREA - {}".format(i)
        print "  Area: {0:.3f}".format(args.area[i])
        print "  Land use: {}".format(landuse[args.landuse[i]])
        print "  Soil type: {}".format(soiltype[args.soiltype[i]])
        print "  K parameter: {0:.3f}".format(ka[i])
        #print "  {0:.3f} * {0:.3f} = {0:.3f}".format(args.area[i], ka[i], args.area[i]*ka[i])
    print ""
    print "The value of the total area is: {0:.3f}".format(area)
    print "The value of k parameter is: {0:.3f}".format(k)
    print "The runoff coefficient is: {0:.3f}".format(runoff_coef)
else:
    print ""
    for i in range(len(args.area)):
        print "{0:.3f}".format(args.area[i])
        print "{}".format(landuse[args.landuse[i]])
        print "{}".format(soiltype[args.soiltype[i]])
        print "{0:.3f}".format(ka[i])
        print ""
    print "k: {0:.3f}".format(k)
    print "Area: {0:.3f}".format(area)
    print "Runoff coefficient: {0:.3f}".format(runoff_coef)
