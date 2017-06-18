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
import inkscapeMadeEasy_Base as inkBase
import inkscapeMadeEasy_Draw as inkDraw
import inkscapeMadeEasy_Plot as inkPlot
import math
import numpy
import os
import StringIO

#---------------------------------------------
class PlotData(inkBase.inkscapeMadeEasy):
  def __init__(self):
    inkex.Effect.__init__(self)

    self.OptionParser.add_option("--tab",action="store", type="string",dest="tab", default="object") 
      
      
    self.OptionParser.add_option("--xData", action="store", type="string", dest="xValues", default='0 1 2 3 4')
    self.OptionParser.add_option("--yData", action="store", type="string", dest="yValues", default='0 1 2 1 0')
    
    self.OptionParser.add_option("--flagUseFile", action="store", type="inkbool", dest="flagUseFile", default=False)
    self.OptionParser.add_option("--fileName", action="store", type="string", dest="fileName", default='')
    self.OptionParser.add_option("--dirName", action="store", type="string", dest="dirName", default='')
    self.OptionParser.add_option("--charSeparator", action="store", type="string", dest="charSeparator", default=' ')
    self.OptionParser.add_option("--skipHeader", action="store", type="inkbool", dest="skipHeader", default=False)
    self.OptionParser.add_option("--headerSize",action="store", type="int",dest="headerSize", default=0)

    self.OptionParser.add_option("--useElipsis", action="store", type="inkbool", dest="useEllipsis", default=False)
    self.OptionParser.add_option("--drawAxis", action="store", type="inkbool", dest="drawAxis", default=False)
    self.OptionParser.add_option("--generalAspectFactor", action="store", type="float", dest="generalAspectFactor", default=1.0) 
         
    self.OptionParser.add_option("--yLimitsFlag", action="store", type="inkbool", dest="yLimitsFlag", default=False)
    self.OptionParser.add_option("--yMin", action="store", type="float", dest="yMin", default='0.0')
    self.OptionParser.add_option("--yMax", action="store", type="float", dest="yMax", default='0.0')
    
    self.OptionParser.add_option("--xLabel", action="store", type="string", dest="xLabel", default='')
    self.OptionParser.add_option("--xScale", action="store", type="float", dest="xScale", default='5')
    self.OptionParser.add_option("--xLog10scale", action="store", type="inkbool", dest="xLog10scale", default=False)
    self.OptionParser.add_option("--xTicks", action="store", type="inkbool", dest="xTicks", default=False)
    self.OptionParser.add_option("--xTickStep", action="store", type="float", dest="xTickStep", default='1')
    self.OptionParser.add_option("--xGrid", action="store", type="inkbool", dest="xGrid", default=True)
    self.OptionParser.add_option("--xExtraText", action="store", type="string", dest="xExtraText", default='')

    self.OptionParser.add_option("--yLabel", action="store", type="string", dest="yLabel", default='')
    self.OptionParser.add_option("--yScale", action="store", type="float", dest="yScale", default='5')
    self.OptionParser.add_option("--yLog10scale", action="store", type="inkbool", dest="yLog10scale", default=False)
    self.OptionParser.add_option("--yTicks", action="store", type="inkbool", dest="yTicks", default=False)
    self.OptionParser.add_option("--yTickStep", action="store", type="float", dest="yTickStep", default='1')
    self.OptionParser.add_option("--yGrid", action="store", type="inkbool", dest="yGrid", default=True)
    self.OptionParser.add_option("--yExtraText", action="store", type="string", dest="yExtraText", default='')
        
  def effect(self):
    
    so = self.options

    # sets the position to the viewport center, round to next 10.
    position=[self.view_center[0],self.view_center[1]]
    position[0]=int(math.ceil(position[0] / 10.0)) * 10
    position[1]=int(math.ceil(position[1] / 10.0)) * 10
    
    #root_layer = self.current_layer
    root_layer = self.document.getroot()
    
    # check if file exists and extract coords data
    filePath=os.path.join(so.dirName, so.fileName).replace('\\','/')
    
    if so.flagUseFile and os.path.isfile(filePath):
      
      s = open(filePath).read().replace(so.charSeparator,' ')
      if so.skipHeader:
        data = numpy.loadtxt(StringIO.StringIO(s),skiprows=so.headerSize)
      else:
        data = numpy.loadtxt(StringIO.StringIO(s))
      XValuesVector=data[:,0].tolist()

      YValuesVector=[]
      for i in range(1,data.shape[1]):
        YValuesVector.append(data[:,i].tolist())
      #self.Dump(YValuesVector,mode='a')
    else:
      #create vector of inputs
      XValuesVector = [float(column) for column in so.xValues.replace(',',' ').split()]
      YValuesVector = [[float(column) for column in so.yValues.replace(',',' ').split()]]  # list of list
              
    # line style
    lineWidthPlot=so.generalAspectFactor*min(so.xScale,so.yScale)/30.0 
    lineColor=inkDraw.color.defined('blue')
    if so.useEllipsis:
      StartLineInf,EndLineInf = inkDraw.marker.createInfLineTicker(self,'InfiniteLine',RenameMode=1,fillColor=lineColor)
      lineStylePlot = inkDraw.lineStyle.set(lineWidth=lineWidthPlot,lineColor=lineColor,markerStart=StartLineInf,markerEnd=EndLineInf)
    else:
      lineStylePlot = inkDraw.lineStyle.set(lineWidth=lineWidthPlot,lineColor=lineColor)

    if so.yLimitsFlag:
      ylim=[so.yMin,so.yMax]
      # check if limits are valid
      if so.yMin >= so.yMax:
        self.displayMsg('Error: yMin and yMax are invalid.')
        return 0
    else:
      ylim=None
        
    for i in range(len(YValuesVector)):
      if so.drawAxis:
        flagDrawAxis=True
      else:
        if i==0:
          flagDrawAxis=True
        else:
          flagDrawAxis=False
      
      if so.yLimitsFlag:      
        # block limits
        
        if sum(y > so.yMax for y in YValuesVector[i])>0:
          inkDraw.text.write(self, 'Some Yvalues are greater than yMax. Clipping value... PLEASE CHECK YOUR PLOT!', [position[0], position[1] + 8], root_layer, fontSize=5)
        if sum(y < so.yMin for y in YValuesVector[i])>0:
          inkDraw.text.write(self, 'Some Yvalues are smaller than yMin. Clipping value... PLEASE CHECK YOUR PLOT!', [position[0], position[1] + 16], root_layer, fontSize=5)     
                
        YValuesVector[i] = [min(y, so.yMax) for y in YValuesVector[i]]
        YValuesVector[i] = [max(y, so.yMin) for y in YValuesVector[i]]
            
      inkPlot.plot.cartesian(self,root_layer,XValuesVector,YValuesVector[i],position,
                            xLabel=so.xLabel,yLabel=so.yLabel,xlog10scale=so.xLog10scale,ylog10scale=so.yLog10scale,
                            xTicks=so.xTicks,yTicks=so.yTicks,xTickStep=so.xTickStep,yTickStep=so.yTickStep,
                            xScale=so.xScale,yScale=so.yScale,xExtraText=so.xExtraText,yExtraText=so.yExtraText,
                            xGrid=so.xGrid,yGrid=so.yGrid,generalAspectFactorAxis=so.generalAspectFactor,lineStylePlot=lineStylePlot,
                            forceYlim=ylim,drawAxis=flagDrawAxis)
                            
if __name__ == '__main__':
  plot = PlotData()
  plot.affect()
    
    