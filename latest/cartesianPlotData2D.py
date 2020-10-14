#!/usr/bin/python

# --------------------------------------------------------------------------------------
#
#    cartesianPlotData2D: - Inkscape extension to plot a set of points, given their coordinates (x,y)
#
#    Copyright (C) 2016 by Fernando Moura
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# --------------------------------------------------------------------------------------

import inkex
import inkscapeMadeEasy.inkscapeMadeEasy_Base as inkBase
import inkscapeMadeEasy.inkscapeMadeEasy_Draw as inkDraw
import inkscapeMadeEasy.inkscapeMadeEasy_Plot as inkPlot
import math
import numpy
import os


# ---------------------------------------------
class PlotData(inkBase.inkscapeMadeEasy):
    def __init__(self):
        inkBase.inkscapeMadeEasy.__init__(self)

        self.arg_parser.add_argument("--tab", type=str, dest="tab", default="object")
        self.arg_parser.add_argument("--subTab_help", type=str, dest="subTab_help", default="object")

        self.arg_parser.add_argument("--xData", type=str, dest="xValues", default='0 1 2 3 4')
        self.arg_parser.add_argument("--yData", type=str, dest="yValues", default='0 1 2 1 0')

        self.arg_parser.add_argument("--filePath", type=str, dest="filePath", default='')
        self.arg_parser.add_argument("--charSeparator", type=str, dest="charSeparator", default=' ')
        self.arg_parser.add_argument("--skipHeader", type=self.bool, dest="skipHeader", default=False)
        self.arg_parser.add_argument("--headerSize", type=int, dest="headerSize", default=0)

        self.arg_parser.add_argument("--useElipsis", type=self.bool, dest="useEllipsis", default=False)
        self.arg_parser.add_argument("--drawAxis", type=self.bool, dest="drawAxis", default=False)
        self.arg_parser.add_argument("--generalAspectFactor", type=float, dest="generalAspectFactor", default=1.0)

        self.arg_parser.add_argument("--yLimitsFlag", type=self.bool, dest="yLimitsFlag", default=False)
        self.arg_parser.add_argument("--yMin", type=float, dest="yMin", default='0.0')
        self.arg_parser.add_argument("--yMax", type=float, dest="yMax", default='0.0')

        self.arg_parser.add_argument("--xLabel", type=str, dest="xLabel", default='')
        self.arg_parser.add_argument("--xScale", type=float, dest="xScale", default='5')
        self.arg_parser.add_argument("--xLog10scale", type=self.bool, dest="xLog10scale", default=False)
        self.arg_parser.add_argument("--xTicks", type=self.bool, dest="xTicks", default=False)
        self.arg_parser.add_argument("--xTickStep", type=float, dest="xTickStep", default='1')
        self.arg_parser.add_argument("--xGrid", type=self.bool, dest="xGrid", default=True)
        self.arg_parser.add_argument("--xExtraText", type=str, dest="xExtraText", default='')

        self.arg_parser.add_argument("--yLabel", type=str, dest="yLabel", default='')
        self.arg_parser.add_argument("--yScale", type=float, dest="yScale", default='5')
        self.arg_parser.add_argument("--yLog10scale", type=self.bool, dest="yLog10scale", default=False)
        self.arg_parser.add_argument("--yTicks", type=self.bool, dest="yTicks", default=False)
        self.arg_parser.add_argument("--yTickStep", type=float, dest="yTickStep", default='1')
        self.arg_parser.add_argument("--yGrid", type=self.bool, dest="yGrid", default=True)
        self.arg_parser.add_argument("--yExtraText", type=str, dest="yExtraText", default='')

    def effect(self):

        so = self.options

        # sets the position to the viewport center, round to next 10.
        position = [self.svg.namedview.center[0], self.svg.namedview.center[1]]
        position[0] = int(math.ceil(position[0] / 10.0)) * 10
        position[1] = int(math.ceil(position[1] / 10.0)) * 10

        # root_layer = self.current_layer
        root_layer = self.document.getroot()
        # root_layer = self.getcurrentLayer()

        # check if file exists and extract coords data

        if os.path.isfile(so.filePath):

            if so.skipHeader:
                data = numpy.loadtxt(so.filePath, delimiter=so.charSeparator, skiprows=so.headerSize)
            else:
                data = numpy.loadtxt(so.filePath, delimiter=so.charSeparator)

            XValuesVector = data[:, 0].tolist()

            YValuesVector = []
            for i in range(1, data.shape[1]):
                YValuesVector.append(data[:, i].tolist())  # self.Dump(YValuesVector,mode='a')
        else:
            # create vector of inputs
            XValuesVector = [float(column) for column in so.xValues.replace(',', ' ').split()]
            YValuesVector = [[float(column) for column in so.yValues.replace(',', ' ').split()]]  # list of list

        # line style
        lineWidthPlot = so.generalAspectFactor * min(so.xScale, so.yScale) / 30.0
        lineColor = inkDraw.color.defined('blue')
        if so.useEllipsis:
            StartLineInf, EndLineInf = inkDraw.marker.createInfLineTicker(self, 'InfiniteLine', RenameMode=1, fillColor=lineColor)
            lineStylePlot = inkDraw.lineStyle.set(lineWidth=lineWidthPlot, lineColor=lineColor, markerStart=StartLineInf, markerEnd=EndLineInf)
        else:
            lineStylePlot = inkDraw.lineStyle.set(lineWidth=lineWidthPlot, lineColor=lineColor)

        if so.yLimitsFlag:
            ylim = [so.yMin, so.yMax]
            # check if limits are valid
            if so.yMin >= so.yMax:
                self.displayMsg('Error: yMin and yMax are invalid.')
                return 0
        else:
            ylim = None

        for i in range(len(YValuesVector)):
            if so.drawAxis:
                flagDrawAxis = True
            else:
                if i == 0:
                    flagDrawAxis = True
                else:
                    flagDrawAxis = False

            if so.yLimitsFlag:
                # block limits

                if sum(y > so.yMax for y in YValuesVector[i]) > 0:
                    inkDraw.text.write(self, 'Some Yvalues are greater than yMax. Clipping value... PLEASE CHECK YOUR PLOT!',
                                       [position[0], position[1] + 8], root_layer, fontSize=5)
                if sum(y < so.yMin for y in YValuesVector[i]) > 0:
                    inkDraw.text.write(self, 'Some Yvalues are smaller than yMin. Clipping value... PLEASE CHECK YOUR PLOT!',
                                       [position[0], position[1] + 16], root_layer, fontSize=5)

                YValuesVector[i] = [min(y, so.yMax) for y in YValuesVector[i]]
                YValuesVector[i] = [max(y, so.yMin) for y in YValuesVector[i]]

            inkPlot.plot.cartesian(self, root_layer, XValuesVector, YValuesVector[i], position, xLabel=so.xLabel, yLabel=so.yLabel,
                                   xlog10scale=so.xLog10scale, ylog10scale=so.yLog10scale, xTicks=so.xTicks, yTicks=so.yTicks, xTickStep=so.xTickStep,
                                   yTickStep=so.yTickStep, xScale=so.xScale, yScale=so.yScale, xExtraText=so.xExtraText, yExtraText=so.yExtraText,
                                   xGrid=so.xGrid, yGrid=so.yGrid, generalAspectFactorAxis=so.generalAspectFactor, lineStylePlot=lineStylePlot,
                                   forceYlim=ylim, drawAxis=flagDrawAxis)


if __name__ == '__main__':
    plot = PlotData()
    plot.run()
    
    
