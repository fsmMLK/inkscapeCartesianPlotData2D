# cartesianPlotData2D

This extension will assist you creating plots from datasets in [Inkscape](https://inkscape.org/).


<img src="docs/images/Examples.png" width="900px"/>

### main features

The main features are

 - linear and log10 scales
 - optional grid lines in X and Y directions
 - adjustable tick mark intervals and sizes
 - optional LaTeX support
 - can optionally read data from text file (csv)

This extension is specially useful when used in conjunction with other mathematical tools like Octave, Matlab, R, etc. to plot data generated by these in Inkscape.

You can either provide data manually in two strings 'X values' and 'Y values' (numbers must be separated by spaces or commas) or via text (.csv) file containing a table of X (column 1) and Y data (column 2,3,...).

In case of data provided via text file, multiple plots can be generated at once by providing Y data of each plot in different columns. The same 'X values' is assumed.

## Current and older versions

Compatibility table

|  Inkscape        |  cartesianPlotData2D | inkscapeMadeEasy | Receive updates?|
|------------------|-----------------|------------------|-----------------|
|       1.0        | 1.0 (latest)    |   1.0 (latest)   | YES             |
| 0.48, 0.91, 0.92 | 0.9x (obsolete) |  0.9x (obsolete) | NO              |


**Latest version:** The latest version of **cartesianPlotData2D** is **1.0**. This version is compatible with Inkscape 1.0 and up only. It is **incompatible** with older Inkscape versions!

**Older versions:** If you have an older version of Inkscape, please use the files under the folder **0.9x** on Github.

**Important: Only the latest version will receive updates, new features, and bug fixes! The usage section in this documentation describes the latest version. In older versions, the disposition of the elements in the plugin's screen might be different. Some features might not be present or have different behavior.**

# Installation and requirements

Installation procedures for latest and older versions are described below.

## Requirements (all versions)

- You will need [inkscapeMadeEasy](https://github.com/fsmMLK/inkscapeMadeEasy) plugin installed. Check the compatibility table above to know the version you need.

## Installation procedure (v1.0 only)

**cartesianPlotData2D** was developed using Inkscape 1.0 in Linux (Kubuntu 18.04). It should work in different OSs too as long as all requirements are met.

1. Install [inkscapeMadeEasy](https://github.com/fsmMLK/inkscapeMadeEasy), **version 1.0** (latest). Follow the instructions in the manual page. **Note:** LaTeX text is used in **cartesianPlotData2D** if the support is activated (nicer results), otherwise regular text elements will be used.

2. **cartesianPlotData2D** installation

    1. Go to Inkscape's extension directory with a file browser. Your inkscape extension directory can be accessed by opening Inkscape and selecting ``Edit > Preferences > System``. Look for the item **User Extensions**  field. There is a button on the right of the field  that will open a file explorer window in that specific folder.

    2. Create a subfolder in the extension directory with the name ``cartesianPlotData2D``. **Important:**  Be careful with upper and lower case letters. You must write as presented above.

    3. Download **cartesianPlotData2D** files and place them inside the directory you just created.

       You don't have to copy all files from Github. The files you will need are inside the ``latest`` folder. In the end you must have the following files and directories in your Inkscape extension directory.

       **LaTeX users:** You can add macros to ``inkscapeMadeEasy/basicLatexPackages.tex``. In this case the same macros will be accessible by all plugins that employ inkscapeMadeEasy.

```
        inkscape
         ┣━━extensions
         ┋   ┣━━ inkscapeMadeEasy      <-- inkscapeMadeEasy folder
             ┃    ┣━━ inkscapeMadeEasy_Base.py
             ┃    ┣━━ inkscapeMadeEasy_Draw.py
             ┃    ┣━━ inkscapeMadeEasy_Plot.py
             ┃    ┗━━ basicLatexPackages.tex
             ┃
             ┣━━ textext               <-- texText folder (if you installed textText)
             ┃    ┋
             ┃
             ┣━━ cartesianPlotData2D        <-- cartesianPlotData2D folder
             ┋    ┣━━ cartesianPlotData2D.inx
                  ┗━━ cartesianPlotData2D.py
        
        NOTE: You might have other sub folders inside the extensions directory. They don't interfere with the plugin.
```

## Installation procedure (v0.9x only)

**cartesianPlotData2D** was developed using Inkscape 0.48 and 0.91 in Linux (Kubuntu 18.04). It should work in different OSs too as long as all requirements are met.

1. Install [inkscapeMadeEasy](https://github.com/fsmMLK/inkscapeMadeEasy), **version 1.0** (latest). Follow the instructions in the manual page. **Note:** LaTeX text is used in **cartesianPlotData2D** if the support is activated (nicer results), otherwise regular text elements will be used.

2. **cartesianPlotData2D** installation

    1. Go to Inkscape's extension directory with a file browser.

    2. Download **cartesianPlotData2D** files and place them inside the directory you just created.

       You don't have to copy all files from Github. The files you will need are inside the ``0.9x`` folder. In the end you must have the following files and directories in your Inkscape extension directory.

        ```
        inkscape
         ┣━━ extensions
         ┋    ┣━━ inkscapeMadeEasy_Base.py
              ┣━━ inkscapeMadeEasy_Draw.py
              ┣━━ inkscapeMadeEasy_Plot.py
              ┃
              ┣━━ textextLib
              ┃    ┣━━ __init__.py
              ┃    ┣━━ basicLatexPackages.tex
              ┃    ┣━━ textext.inx
              ┃    ┗━━ textext.py
              ┃
              ┣━━ cartesianPlotData2D.inx        <--   from repository folder 0.9x!
              ┗━━ cartesianPlotData2D.py         <--
        ```

# Usage

The extension can be found under `extensions > fsmMLK > Plot 2D > Cartesian` menu.

This extension is presented in two tabs, **Dataset** and  **Config**. The first is used to pass the data set and provide general configuration options. The second is used to configure the axes.

## Dataset tab

Here you set the dataset and adjust several general parameters. The dataset can be a file containing tabulated data (.csv)  or provided manually in two strings.

<img src="docs/images/GenaralConfig_tab.png" width="450px"/>

This tab contains 3 sections, described below. 

### File dataset section

If the dataset is in a tabulated text (.csv) file, use this section.

**File:** Here you can select the file containing the data (.txt or .csv). The expected file format is explained below.

The text file must be organized as a table of values. The first column must contain X datas and Y data must be stores in subsequent columns. All columns must have the same number of lines.

The file can have a header with an arbitrary number of lines. In such case, you must inform the number of lines to be skipped (see below).

The separator can be any character, except the following characters: `.` (dot), `+` (plus), `-`(minus), `E`, `e`. The values can be integer or float values in decimal or exponential notation (e.g. the value 120 can also be given as 1.2e+2)

> Attention: The decimal separator must be `.` (dot). If your computer uses comma, you should fix you computer =]

Example 1: (delimited by spaces)
```
-2 4
-1 2
 0 0
 1 2
 2 4
```
the extension will create one plot. The first column is X and the second Y data.

Example 2: (delimited by semicolons, with a header containing 3 lines)
```
Hello, this is my header
second line
another one!
-2;4;0
-1;2;1
 0;0;2
 1;2;3
 2;4;4
```
the extension will create two graphs, where:
  - the first  plot will use the first column as X data and the second as Y data
  - the second plot will use the first column as X data and the third  as Y data

**Delimiter character:** Character used to delimit the columns of the file. If no character is informed, space is assumed

**Skip header lines:** Inform that the file contains a header. On the side there is a field to inform the number of lines of the header.

### Manual dataset section

**Atention: Manual dataset is used only if no text file is passed to the extension.**

**X values:** String containing X values of each point. The values must be separated by space or comma. 'X values' and 'Y values' must have the same number of values.

**Y values:** String containing Y values of each point. The values must be separated by space or comma. 'X values' and 'Y values' must have the same number of values.

### Custom output range section


**Use custom output range:** Toggle custom Y axis range. If unchecked the limits will be defined by the limits of the input data.

**Y limits:** (linear scale only) Set the range of the dependent variable (Y axis), despite of the data. On the side there are two fields for the lower and upper limits.

If Ydata has values outside the specified custom limits, then the plot will be clipped at these values. A text element will be added to the document informing it. Check your plot! See image bellow.

<img src="docs/images/yMin_yMax.png" width="600px"/>

## Config tab

This tab has two sections. The first contains general properties of the plot and the second controls the axes.

<img src="docs/images/AxesConfig_Tab.png" width="450px"/>


### General config section

**Use ellipsis marks at the ends:** Use ellipsis marks at the end of the plots to indicate continuation

<img src="docs/images/ellipsis.png" width="250px"/>

**Draw Cartesian plane for each dataset:** This option affects only multiple plots via input file. If checked, each plot will have its own Cartesian plane. Otherwise only the first plot will have it.

**General aspect factor:** General aspect ratio between line widths and text height. I designed this extension to have an overall aspect ratio that "looks nice". It is a function of X and Y tick lengths. With this control you can scale both line width and text height. The defauls value is 1.0.

<img src="docs/images/generalAspectRatio.png" width="600px"/>

### Axes section

The parameters in this section controls X and Y axes. They act on the axes the same way.

**Label:** label of the axes. If LaTeX support is activated and you want to write in mathematical environment, enclose your text with $...$.

> Tip: Since `siunitx` package is included in inkscapeMadeEasy's basicLatexPackages.tex, you can use any unit command available there too!

> Ex: `Foobar $\sqrt{x^2}$ so fancy! (\si{\newton\per\squaremetre})`

<img src="docs/images/Legend_01.png" width="400px"/>

**Log scale:** Set the axis to be represented in log10 scale.

**Add grid:** Draw grid lines.

   - *linear scale:* The grid lines will be placed at the tick marks.
   - *log scale:* The grid lines will be placed dividing each decade in 10 parts

**Add ticks:** Draw tick marks with associated values. 

**Tick step:** Tick mark interval, in units of your chart. This option does not affect log scale.

Ex: limits from -1 to 1, with tick step of 0.5 will produce ticks at -1, -0.5, 0, 0.5, 1

> Note: The ticks will radiate from the origin (x=0 or y=0) unless the origin does not lie within the limits. In such cases, the ticks will radiate starting from the limit closest to the origin. See image below.
>
> Examples in x direction: (The same rules apply to Y direction)
>
> <img src="docs/images/TickStep.png" width="500px"/>


**Tick length** The distance between tick marks, in units of your canvas. See image below.

   - *linear scale:* The distance between consecutive ticks, in units of your canvas.
   - *logarithmic scale:* The size of each decade, in units of your canvas.

<img src="docs/images/TickLength.png" width="350px"/>

**Tick suffix:** Optional extra suffix to be added to tick text. **LaTeX support enabled**: You can use any LaTeX text/commands valid in mathematical environment. You don't have to enclose your text between $...$.

**Atention**: the values appended to tick mark text will NOT affect input/output limits!

<img src="docs/images/TickSuffix.png" width="700px"/> 

# Observations

 - The plot is generated by evaluating the function at points along the input range and connecting them with a polyline. Therefore if your function has discontinuities, your plot will present a line connecting both sides of the discontinuity. **In such cases, please check your plot!**  ;)

<img src="docs/images/Obs_discontinuous.png" width="600px"/>

 - This extension does not check if your file contains ``NaN`` or ``Inf`` values. Check your data before using the extension.

 - The axes will be placed crossing the origin (0,0) or crossing the coordinate (x,y) closest to the origin if the origin does not lies within the limits.
 - The axes will be created in the center of your screen.

