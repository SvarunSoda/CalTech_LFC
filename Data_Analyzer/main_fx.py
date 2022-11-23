#### MAIN FUNCTION DEFINITIONS ####

#### BASE IMPORTS ####
import sys
import os
import ctypes
from ctypes import c_long, c_wchar_p, c_ulong, c_void_p

#### MY IMPORTS ####
data_fx = None
math_fx = None
flattening_fx = None
graphing_fx = None
utils_fx = None

#### GLOBAL VARIABLES ####
Gen_ProgramName = "CalTech - LFC Data Analyzer Program"
Gen_ProgramVersion = 0.16
Gen_MaxCharsPerLine = 115
Gen_LineEnumLen = 5
Gen_FancyLoading = False
Gen_CursorPosFileName = "cursor.txt"
Gen_GHandle = ctypes.windll.kernel32.GetStdHandle(c_long(-11))

Gen_WorkingDirectory = None                         #0
Gen_GraphConfig = [                                 
    None,           #Gen_GraphSizeX                 11
    None,           #Gen_GraphSizeY                 12
    None,           #Gen_GraphDPI                   13
    None,           #Gen_GraphLineMarkerSize        14
    None,           #Gen_GraphInnerScaleX           15
    None,           #Gen_GraphLegendPosX            16
    None,           #Gen_GraphLegendPosY            17
    None,           #Gen_GraphLegendSizeRatio       18
    None,           #Gen_GraphLegendMaxSize         19
    None,           #Gen_GraphLegendTextMaxLength   23
    None            #Gen_GraphSaveExtension         21
    ]

Prog2_GaussianSigma = None                          #1
Prog2_GaussianPhis = []                             #22
Prog2_DataDirectory = None                          #8
Prog2_GraphViewport = [
    [None, None],                                   #9, 10
    [None, None]                                    #24, 25
    ]
Prog2_GraphData = []                                #20
Prog2_GraphDataFlatten = []                         #2
Prog2_GraphDataSkips = []                           #26
Prog2_GraphDataFits = []                            #27
Prog2_GraphDataPeakFinds = []                       #28

#### MAIN PROGRAM FUNCTIONS ####
def main():
#{
    Main_DeleteFile(os.getcwd().replace("\\", Main_GetPathSeparator()) + Main_GetPathSeparator() + Gen_CursorPosFileName)

    Main_InitProgram()
    Main_VersionPrints()

    Main_ProgramDataAnalyzer()

    Main_StatusPrint("---- PROGRAM EXITED ----", 2)
#}

def Main_ProgramDataAnalyzer(): #2
#{
    displayGraphs = False
    saveGraphs = False
    saveReports = False
    namingIdx = -1

    userInput = Main_Input("Do you want the resulting graphs to be displayed to you after graphing? (enter \"Y\" for Yes, anything else for No)\n\nYour answer: ")

    if (userInput == "Y") or (userInput == "y"):
        displayGraphs = True

    userInput = Main_Input("\nDo you want the resulting graphs to be saved after graphing? (enter \"Y\" for Yes, anything else for No)\n\nYour answer: ")

    if (userInput == "Y") or (userInput == "y"):
    #{
        saveGraphs = True

        userInput = Main_Input("\nAfter which index of the data do you want the resulting plot image files to be named after (enter an integer value)?\n\nYour answer: ")

        if (Main_IsStringNum(userInput, 0) == True):
            namingIdx = int(userInput)
    #}

    userInput = Main_Input("\nDo you want any resulting Gaussian fits to be saved in a report file? (enter \"Y\" for Yes, anything else for No)\n\nYour answer: ")

    if (userInput == "Y") or (userInput == "y"):
        saveReports = True

    Main_Print(" ")

    peakFindDataX = []
    peakFindDataY = []

    for i in range(len(Prog2_GraphData)):
    #{
        currDataNames = Prog2_GraphData[i]
        currFlatteningData = Prog2_GraphDataFlatten[i]
        currDataSkips = Prog2_GraphDataSkips[i]
        currDataFits = Prog2_GraphDataFits[i]
        currDataPeakFinds = Prog2_GraphDataPeakFinds[i]
        
        if (len(currDataNames) == 0):
            continue

        dataLabels = []
        data = data_fx.Data_LoadDataFromFiles(Prog2_DataDirectory, 
                                              currDataNames, 
                                              dataLabels, 
                                              currFlatteningData, 
                                              currDataSkips)

        xData = []
        yData = []
       
        data_fx.Data_SeparateXYData(data, xData, yData)

        newCurrDataSkips = []
        newCurrFlatteningData = []
        Main_ResizeList(newCurrDataSkips, len(dataLabels))
        Main_ResizeList(newCurrFlatteningData, len(dataLabels))

        data_fx.Data_PerformOperatorsOnData(xData, 
                                            yData, 
                                            currDataNames, 
                                            dataLabels, 
                                            [currFlatteningData, newCurrFlatteningData], 
                                            [currDataSkips, newCurrDataSkips])

        flattening_fx.Math_FlattenDatas(xData, 
                                        yData, 
                                        [Prog2_GraphViewport[0][0], Prog2_GraphViewport[0][1]], 
                                        newCurrFlatteningData)

        xViews = [utils_fx.Utils_MinOfLists(xData), utils_fx.Utils_MaxOfLists(xData)]
        yViews = [(utils_fx.Utils_MinOfLists(yData) - 10), (utils_fx.Utils_MaxOfLists(yData) + 10)]

        for j in range(len(currDataPeakFinds)):
        #{
            if (currDataPeakFinds[j] == 1):
            #{
                peakFindDataX.append(xData[j])
                peakFindDataY.append(yData[j])
            #}
        #}

        gaussianSigmas = []
        gaussianPhis = []
        gaussianAmplitudes = []

        for j in range(len(Prog2_GaussianPhis)):
        #{
            gaussianSigmas.append(Prog2_GaussianSigma)
            gaussianPhis.append(Prog2_GaussianPhis[j])
            gaussianAmplitudes.append(1)
        #}

        reportSavePath = ""
        reportFileName = ""

        if (saveReports == True):
        #{
            reportSavePath = (Prog2_DataDirectory + "reports" + Main_GetPathSeparator())
            reportFileName = "GaussianFit_Report_"
        #}

        data_fx.Data_FitGaussiansToDatas(xData, 
                                         yData, 
                                         gaussianSigmas, 
                                         gaussianPhis, 
                                         1300, 1900, 
                                         0, 
                                         gaussianAmplitudes, 
                                         1420, 
                                         dataLabels, 
                                         newCurrFlatteningData, newCurrDataSkips, currDataFits, 
                                         True,
                                         i, 
                                         reportSavePath, reportFileName)

        if (len(dataLabels) != len(xData)):
            raise ValueError("The size of the data labels and the amount of data aren't equal!")

        saveDirectory = ""

        if (saveGraphs == True):
        #{
            saveDirectory = Prog2_DataDirectory + "plots" + Main_GetPathSeparator()

            if (namingIdx == -1) or (namingIdx >= len(currDataNames)):
                saveDirectory += "Plot_" + str(i)
            else:
                saveDirectory += dataLabels[namingIdx]
        #}

        if (Prog2_GraphViewport[0][0] != None):
            xViews[0] = Prog2_GraphViewport[0][0]
        if (Prog2_GraphViewport[0][1] != None):
            xViews[1] = Prog2_GraphViewport[0][1]
        if (Prog2_GraphViewport[1][0] != None):
            yViews[0] = Prog2_GraphViewport[1][0]
        if (Prog2_GraphViewport[1][1] != None):
            yViews[1] = Prog2_GraphViewport[1][1]

        graphing_fx.Graphing_GraphDataPoints(xData, yData, 
                                            xViews, 
                                            yViews, 
                                            dataLabels,
                                            newCurrDataSkips,
                                            [Gen_ProgramName + " v" + str(Gen_ProgramVersion), "Spectrum (nm)", "Level (db)"],
                                            Gen_GraphConfig, 
                                            False,
                                            None, 
                                            [False, False],
                                            displayGraphs, saveDirectory, "")
    #}

    #data_fx.Data_IdentifyHighPeak(peakFindDataX, peakFindDataY, Prog2_GraphViewport[0], round(len(peakFindDataX) / 2), "HighPeakReport.txt", (Prog2_DataDirectory + "reports" + Main_GetPathSeparator()))

    if (len(peakFindDataX) > 0):
    #{
        gaussianSigmas = []
        gaussianPhis = []
        gaussianAmplitudes = []

        for j in range(len(Prog2_GaussianPhis)):
        #{
            gaussianSigmas.append(Prog2_GaussianSigma)
            gaussianPhis.append(Prog2_GaussianPhis[j])
            gaussianAmplitudes.append(1)
        #}

        peakFindDatasX = []
        peakFindDatasY = []
        mus = None

        utils_fx.Utils_CheckEqualListSizes(peakFindDataX)
        utils_fx.Utils_CheckEqualListSizes(peakFindDataY)

        for j in range(len(peakFindDataX)):
        #{
            peakFindDatasX.append([peakFindDataX[j]])
            peakFindDatasY.append([peakFindDataY[j]])

            mus = data_fx.Data_FitGaussiansToDatas(peakFindDatasX[j], 
                                             peakFindDatasY[j], 
                                             gaussianSigmas, 
                                             gaussianPhis, 
                                             1300, 1900, 
                                             0, 
                                             gaussianAmplitudes, 
                                             1420, 
                                             [], 
                                             [], [], [], 
                                             False,
                                             0, 
                                             "", "")

            del peakFindDatasX[len(peakFindDatasX) - 1][0]
        #}

        graphSingleGaussian = False
        scatterPlot = False
        mus = mus[0]
        amplitudeTitles = []
        peakFindDataLabels = []

        for j in range(len(mus)):
        #{
            amplitudeTitles.append("Gaussian Position #" + str(j) + " (" + str(round(mus[j])) + ")")

            if (graphSingleGaussian == True):
                peakFindDataLabels.append(["Gaussian #" + str(j) + " (mu = " + str(round(mus[j])) + ")"])
            else:
                peakFindDataLabels.append("Gaussian #" + str(j) + " (mu = " + str(round(mus[j])) + ")")
        #}

        Main_StatusPrint("Attempting to acquire Gaussian amplitude graph data...", 0)

        amplitudeDataX = []
        amplitudeDataY = []
        numVoltages = len(peakFindDatasX)
        iterations = None

        for l in range(len(mus)):
        #{
            currAmplitudeDataX = []
            currAmplitudeDataY = []

            for j in range(numVoltages):
            #{
                for k in range(len(peakFindDatasX[j])):
                #{
                    if ((graphSingleGaussian == True) and (k != l)):
                        continue

                    currAmplitudeDataX.append(j)
                    currAmplitudeDataY.append(peakFindDatasY[j][k][utils_fx.Utils_FindInList(peakFindDatasX[j][k], math_fx.Math_GetClosestNum(mus[l], peakFindDatasX[j][k]))])
                #}
            #}

            iterations = len(currAmplitudeDataX) / numVoltages

            if (iterations.is_integer() == False):
                raise ValueError("Number of iterations isn't an integer!")

            iterations = int(iterations)
            idx = 0

            while (idx < iterations):
            #{
                insAmplitudeDataX = []
                insAmplitudeDataY = []

                for j in range(numVoltages):
                #{
                    insAmplitudeDataX.append(currAmplitudeDataX[idx + (j * iterations)])
                    insAmplitudeDataY.append(currAmplitudeDataY[idx + (j * iterations)])
                #}

                amplitudeDataX.append(insAmplitudeDataX)
                amplitudeDataY.append(insAmplitudeDataY)

                idx += 1
            #}
        #}

        Main_StatusPrint("Successfully acquired Gaussian amplitude graph data.", 1)

        data_fx.Data_CheckSeparatedXYData(amplitudeDataX, amplitudeDataY)

        xMargins = 0.5
        yMargins = (utils_fx.Utils_MaxOfLists(amplitudeDataY) - utils_fx.Utils_MinOfLists(amplitudeDataY)) / 8
        xViews = [utils_fx.Utils_MinOfLists(amplitudeDataX) - xMargins, utils_fx.Utils_MaxOfLists(amplitudeDataX) + xMargins]
        yViews = [utils_fx.Utils_MinOfLists(amplitudeDataY) - yMargins, utils_fx.Utils_MaxOfLists(amplitudeDataY) + yMargins]

        idx = 0
        graphIdx = 0

        while (idx < len(amplitudeDataX)):
        #{
            currAmplitudeGraphDataX = []
            currAmplitudeGraphDataY = []

            for j in range(iterations):
            #{
                currAmplitudeGraphDataX.append(amplitudeDataX[idx + j])
                currAmplitudeGraphDataY.append(amplitudeDataY[idx + j])
            #}

            currAmplitudeDataSkips = []

            for j in range(len(currAmplitudeGraphDataX)):
                currAmplitudeDataSkips.append(1)

            currAmplitudeSaveDirectory = ""

            if (saveGraphs == True):
                currAmplitudeSaveDirectory = Prog2_DataDirectory + "plots" + Main_GetPathSeparator() + "AmplitudeVoltage_Plot_" + str(graphIdx)

            currAmplitudeDataLabels = peakFindDataLabels

            if (graphSingleGaussian == True):
                currAmplitudeDataLabels = peakFindDataLabels[graphIdx]

            graphing_fx.Graphing_GraphDataPoints(currAmplitudeGraphDataX, currAmplitudeGraphDataY, 
                                                xViews, 
                                                yViews, 
                                                currAmplitudeDataLabels,
                                                currAmplitudeDataSkips,
                                                [Gen_ProgramName + " v" + str(Gen_ProgramVersion) + "\n" + amplitudeTitles[graphIdx], "Voltage (V)", "Amplitude (db)"],
                                                Gen_GraphConfig, 
                                                scatterPlot,
                                                None,
                                                [True, False],
                                                displayGraphs, currAmplitudeSaveDirectory, currAmplitudeSaveDirectory)

            idx += iterations
            graphIdx += 1
        #}

        amplitudeDataSkips = []

        for j in range(len(amplitudeDataX)):
            amplitudeDataSkips.append(1)

        amplitudeSaveDirectory = ""

        if (saveGraphs == True):
            amplitudeSaveDirectory = Prog2_DataDirectory + "plots" + Main_GetPathSeparator() + "AmplitudeVoltage_Plot_All"

        allAmplitudeDataLabels = peakFindDataLabels

        if (graphSingleGaussian == True):
        #{
            allAmplitudeDataLabels = []

            for j in range(len(peakFindDataLabels)):
                allAmplitudeDataLabels.append(peakFindDataLabels[j][0])
        #}

        graphing_fx.Graphing_GraphDataPoints(amplitudeDataX, amplitudeDataY, 
                                            xViews,
                                            yViews,
                                            allAmplitudeDataLabels,
                                            amplitudeDataSkips,
                                            [Gen_ProgramName + " v" + str(Gen_ProgramVersion) + "\nAll Gaussian Positions", "Voltage (V)", "Amplitude (db)"],
                                            Gen_GraphConfig, 
                                            scatterPlot,
                                            None, 
                                            [True, False],
                                            displayGraphs, amplitudeSaveDirectory, amplitudeSaveDirectory)
    #}
#}

#### SUPPORTING FUNCTIONS ####

def Main_InitProgram():
#{
    Main_AssignGlobalVariablesFromFile("config.txt")
    Main_CheckDirectory(Gen_WorkingDirectory)
    Main_ImportOtherFiles()
#}

def Main_AssignGlobalVariablesFromFile(fileName):
#{
    while (True):
    #{
        Main_ResetGlobalVariables()

        global Gen_WorkingDirectory
        global Gen_GraphConfig

        global Prog2_GaussianSigma
        global Prog2_GaussianPhis
        global Prog2_DataDirectory
        global Prog2_GraphViewport
        global Prog2_GraphData
        global Prog2_GraphDataFlatten

        Main_CheckFile(fileName)

        file = open(fileName, "r+")

        Main_StatusPrint("Attempting to gather parameters from config file...", 0)

        assignedVariableIDs = []

        while (True):
        #{
            line = file.readline()

            if not (line):
                break

            wordBuff = ""
            waitingForValue = False

            for i in range(len(line)):
            #{
                currChar = line[i]
                foundSpace = False

                if (currChar == ' ') or (currChar == '\t') or (currChar == '\n'):
                    foundSpace = True
                elif (currChar == '"') or (currChar == '\''):
                    continue
                elif (currChar == '#'):
                    break
                else:
                    wordBuff += currChar

                if (waitingForValue == False):
                #{
                    foundID = None

                    if (wordBuff == "Gen_WorkingDirectory"):
                        foundID = 0
                    elif (wordBuff == "Gen_GraphSizeX"):    
                        foundID = 11
                    elif (wordBuff == "Gen_GraphSizeY"):    
                        foundID = 12
                    elif (wordBuff == "Gen_GraphDPI"):    
                        foundID = 13
                    elif (wordBuff == "Gen_GraphLineMarkerSize"):    
                        foundID = 14
                    elif (wordBuff == "Gen_GraphInnerScaleX"):    
                        foundID = 15
                    elif (wordBuff == "Gen_GraphLegendPosX"):    
                        foundID = 16
                    elif (wordBuff == "Gen_GraphLegendPosY"):    
                        foundID = 17
                    elif (wordBuff == "Gen_GraphLegendSizeRatio"):    
                        foundID = 18
                    elif (wordBuff == "Gen_GraphLegendMaxSize"):    
                        foundID = 19
                    elif (wordBuff == "Gen_GraphLegendTextMaxLength"):    
                        foundID = 23
                    elif (wordBuff == "Gen_GraphSaveExtension"):    
                        foundID = 21
                    elif (wordBuff == "Prog2_GaussianSigma"):    
                        foundID = 1
                    elif (wordBuff == "Prog2_GaussianPhis"):
                        foundID = 22
                    elif (wordBuff == "Prog2_DataDirectory"):
                        foundID = 8
                    elif (wordBuff == "Prog2_GraphViewportX1"):
                        foundID = 9
                    elif (wordBuff == "Prog2_GraphViewportX2"):
                        foundID = 10
                    elif (wordBuff == "Prog2_GraphViewportY1"):
                        foundID = 24
                    elif (wordBuff == "Prog2_GraphViewportY2"):
                        foundID = 25
                    elif (wordBuff == "Prog2_GraphData"):
                        foundID = 20

                    if (foundID != None):
                    #{
                        waitingForValue = True    
                        assignedVariableIDs.append(foundID)
                        wordBuff = ""
                    #}
                    elif (foundSpace == True) and (len(wordBuff) > 0):
                    #{
                        raise ValueError("Unknown identifier found in config file!")
                    #}
                #}
                else:
                #{
                    if (len(wordBuff) > 0) and (wordBuff[0] == '='):
                    #{
                        if (len(wordBuff) > 1) and (foundSpace == True):
                        #{
                            value = ""
                        
                            for i in range(len(wordBuff) - 1):
                                value += wordBuff[i + 1]

                            lastVariableID = assignedVariableIDs[len(assignedVariableIDs) - 1]

                            if (lastVariableID == 0):
                            #{
                                Gen_WorkingDirectory = value
                            #}
                            elif (lastVariableID == 11):
                            #{
                                if (Main_IsStringNum(value, 1) == False):
                                    raise ValueError("Gen_GraphConfig[0] was expecting a numerical value!")

                                Gen_GraphConfig[0] = float(value)
                            #}
                            elif (lastVariableID == 12):
                            #{
                                if (Main_IsStringNum(value, 1) == False):
                                    raise ValueError("Gen_GraphConfig[1] was expecting a numerical value!")

                                Gen_GraphConfig[1] = float(value)
                            #}
                            elif (lastVariableID == 13):
                            #{
                                if (Main_IsStringNum(value, 0) == False):
                                    raise ValueError("Gen_GraphConfig[2] was expecting a numerical value!")

                                Gen_GraphConfig[2] = int(value)
                            #}
                            elif (lastVariableID == 14):
                            #{
                                if (Main_IsStringNum(value, 0) == False):
                                    raise ValueError("Gen_GraphConfig[3] was expecting a numerical value!")

                                Gen_GraphConfig[3] = int(value)
                            #}
                            elif (lastVariableID == 15):
                            #{
                                if (Main_IsStringNum(value, 1) == False):
                                    raise ValueError("Gen_GraphConfig[4] was expecting a numerical value!")

                                Gen_GraphConfig[4] = float(value)
                            #}
                            elif (lastVariableID == 16):
                            #{
                                if (Main_IsStringNum(value, 1) == False):
                                    raise ValueError("Gen_GraphConfig[5] was expecting a numerical value!")

                                Gen_GraphConfig[5] = float(value)
                            #}
                            elif (lastVariableID == 17):
                            #{
                                if (Main_IsStringNum(value, 1) == False):
                                    raise ValueError("Gen_GraphConfig[6] was expecting a numerical value!")

                                Gen_GraphConfig[6] = float(value)
                            #}
                            elif (lastVariableID == 18):
                            #{
                                if (Main_IsStringNum(value, 0) == False):
                                    raise ValueError("Gen_GraphConfig[7] was expecting a numerical value!")

                                Gen_GraphConfig[7] = int(value)
                            #}
                            elif (lastVariableID == 19):
                            #{
                                if (Main_IsStringNum(value, 0) == False):
                                    raise ValueError("Gen_GraphConfig[8] was expecting a numerical value!")

                                Gen_GraphConfig[8] = int(value)
                            #}
                            elif (lastVariableID == 23):
                            #{
                                if (Main_IsStringNum(value, 0) == False):
                                    raise ValueError("Gen_GraphConfig[9] was expecting a numerical value!")

                                Gen_GraphConfig[9] = int(value)
                            #}
                            elif (lastVariableID == 21):
                            #{
                                Gen_GraphConfig[10] = value
                            #}
                            elif (lastVariableID == 8):
                            #{
                                Prog2_DataDirectory = value
                            #}
                            elif (lastVariableID == 1):
                            #{
                                if (Main_IsStringNum(value, 1) == False):
                                    raise ValueError("Prog2_GaussianSigma was expecting a numerical value!")

                                Prog2_GaussianSigma = float(value)
                            #}
                            elif (lastVariableID == 22):
                            #{
                                if (Main_IsStringNum(value, 1) == False):
                                    raise ValueError("Prog2_GaussianPhis was expecting a numerical value!")

                                Prog2_GaussianPhis.append(float(value))
                            #}
                            elif (lastVariableID == 9):
                            #{
                                if (Main_IsStringNum(value, 1) == False):
                                    raise ValueError("Prog2_GraphViewportX1 was expecting a numerical value!")

                                Prog2_GraphViewport[0][0] = float(value)
                            #}
                            elif (lastVariableID == 10):
                            #{
                                if (Main_IsStringNum(value, 1) == False):
                                    raise ValueError("Prog2_GraphViewportX2 was expecting a numerical value!")

                                Prog2_GraphViewport[0][1] = float(value)
                            #}
                            elif (lastVariableID == 24):
                            #{
                                if (Main_IsStringNum(value, 1) == False):
                                    raise ValueError("Prog2_GraphViewportY1 was expecting a numerical value!")

                                Prog2_GraphViewport[1][0] = float(value)
                            #}
                            elif (lastVariableID == 25):
                            #{
                                if (Main_IsStringNum(value, 1) == False):
                                    raise ValueError("Prog2_GraphViewportY2 was expecting a numerical value!")

                                Prog2_GraphViewport[1][1] = float(value)
                            #}
                            elif (lastVariableID == 20):
                            #{
                                dataSkip = 1
                                dataSkipIdxPos = value.find("//")

                                if (dataSkipIdxPos != -1):
                                #{
                                    dataSkip = 0
                                    value = value.replace("//", "")
                                #}

                                dataFitPos = value.find("?")
                                dataFit = 0

                                if (dataFitPos != -1):
                                #{
                                    dataFit = 1
                                    value = value.replace("?", "")
                                #}

                                dataPeakFindPos = value.find("\\")
                                dataPeakFind = 0

                                if (dataPeakFindPos != -1):
                                #{
                                    dataPeakFind = 1
                                    value = value.replace("\\", "")
                                #}

                                plotIdxPos = value.find("|")
                                flattenIdxPos = value.find(":")
                                plotIdx = 0
                                flattenIdx = -1
                                flattenArgs = []
                                plotFileName = ""

                                if (plotIdxPos == -1):
                                #{
                                    raise ValueError("No plot index separator \"|\" found in a graph data entry!")
                                #}
                                else:
                                #{
                                    plotIdxPosEnd = len(value)

                                    if (flattenIdxPos != -1):
                                    #{
                                        if (flattenIdxPos == (len(value) - 1)):
                                            raise ValueError("No index found after \":\" separator!")

                                        plotIdxPosEnd = flattenIdxPos
                                        flattenIdxStr = value[(plotIdxPosEnd + 1) : len(value)]

                                        flattenArgsStartPos = flattenIdxStr.find("(")
                                        flattenArgsEndPos = flattenIdxStr.find(")")

                                        if (flattenArgsStartPos != -1) or (flattenArgsEndPos != -1):
                                        #{
                                            if (flattenArgsStartPos == -1):
                                                raise ValueError("Missing \"(\" in the flatten arguments! (an unintended space after a comma in the flatten arguments may have been inserted)")
                                            if (flattenArgsEndPos == -1):
                                                raise ValueError("Missing \")\" in the flatten arguments! (an unintended space after a comma in the flatten arguments may have been inserted)")

                                            flattenArgsStr = flattenIdxStr[(flattenArgsStartPos + 1) : flattenArgsEndPos]
                                            argBuff = ""

                                            for i in range(len(flattenArgsStr)):
                                            #{
                                                currChar = flattenArgsStr[i]

                                                if (currChar == ' ') or (currChar == '\t'):
                                                #{
                                                    continue
                                                #}
                                                elif (currChar == ','):
                                                #{
                                                    if (Main_IsStringNum(argBuff, 1) == False):
                                                        raise ValueError("One of the flatten arguments is not a number!")

                                                    flattenArgs.append(float(argBuff))
                                                    argBuff = ""
                                                #}
                                                else:
                                                #{
                                                    argBuff += currChar
                                                #}
                                            #}

                                            if (Main_IsStringNum(argBuff, 1) == True):
                                                flattenArgs.append(float(argBuff))

                                            argBuff = ""

                                            flattenIdxStr = flattenIdxStr[0 : flattenArgsStartPos]
                                        #}

                                        if (Main_IsStringNum(flattenIdxStr, 0) == False):
                                            raise ValueError("One of the flatten index values is not a number!")

                                        flattenIdx = int(flattenIdxStr)
                                    #}

                                    plotIdxStr = value[(plotIdxPos + 1) : plotIdxPosEnd]

                                    if (Main_IsStringNum(plotIdxStr, 0) == False):
                                        raise ValueError("One of the plot index values is not a number!")

                                    plotIdx = int(plotIdxStr)
                                    plotFileName = value[0 : plotIdxPos]
                                #}

                                flattenData = [flattenIdx]

                                for i in range(len(flattenArgs)):
                                    flattenData.append(flattenArgs[i])

                                Main_ResizeList(Prog2_GraphData, (plotIdx + 1))
                                Main_ResizeList(Prog2_GraphDataFlatten, (plotIdx + 1))
                                Main_ResizeList(Prog2_GraphDataSkips, (plotIdx + 1))
                                Main_ResizeList(Prog2_GraphDataFits, (plotIdx + 1))
                                Main_ResizeList(Prog2_GraphDataPeakFinds, (plotIdx + 1))

                                Prog2_GraphData[plotIdx].append(plotFileName)
                                Prog2_GraphDataFlatten[plotIdx].append(flattenData)
                                Prog2_GraphDataSkips[plotIdx].append(dataSkip)
                                Prog2_GraphDataFits[plotIdx].append(dataFit)
                                Prog2_GraphDataPeakFinds[plotIdx].append(dataPeakFind)
                            #}

                            waitingForValue = False
                            wordBuff = ""
                        #}
                    #}
                #}
            #}
        #}

        file.close()

        if not (0 in assignedVariableIDs):
        #{
            Gen_WorkingDirectory = os.getcwd()
            Gen_WorkingDirectory = Gen_WorkingDirectory.replace("\\", Main_GetPathSeparator())

            if (Gen_WorkingDirectory[len(Gen_WorkingDirectory) - 1] != Main_GetPathSeparator()):
                Gen_WorkingDirectory += Main_GetPathSeparator()

            Main_StatusPrint("Gen_WorkingDirectory was not found in the config file, defaulting to the same directory as the program.", 4)
        #}
        if not (11 in assignedVariableIDs):
        #{
            Main_ErrorPrompt("Gen_GraphSizeX was not found in the config file!\n\nPress any key to retry...")
        
            continue
        #}
        if not (12 in assignedVariableIDs):
        #{
            Main_ErrorPrompt("Gen_GraphSizeY was not found in the config file!\n\nPress any key to retry...")
        
            continue
        #}
        if not (13 in assignedVariableIDs):
        #{
            Main_ErrorPrompt("Gen_GraphDPI was not found in the config file!\n\nPress any key to retry...")
        
            continue
        #}
        if not (14 in assignedVariableIDs):
        #{
            Main_ErrorPrompt("Gen_GraphLineMarkerSize was not found in the config file!\n\nPress any key to retry...")
        
            continue
        #}
        if not (15 in assignedVariableIDs):
        #{
            Main_ErrorPrompt("Gen_GraphInnerScaleX was not found in the config file!\n\nPress any key to retry...")
        
            continue
        #}
        if not (16 in assignedVariableIDs):
        #{
            Main_ErrorPrompt("Gen_GraphLegendPosX was not found in the config file!\n\nPress any key to retry...")
        
            continue
        #}
        if not (17 in assignedVariableIDs):
        #{
            Main_ErrorPrompt("Gen_GraphLegendPosY was not found in the config file!\n\nPress any key to retry...")
        
            continue
        #}
        if not (18 in assignedVariableIDs):
        #{
            Main_ErrorPrompt("Gen_GraphLegendSizeRatio was not found in the config file!\n\nPress any key to retry...")
        
            continue
        #}
        if not (19 in assignedVariableIDs):
        #{
            Main_ErrorPrompt("Gen_GraphLegendMaxSize was not found in the config file!\n\nPress any key to retry...")
        
            continue
        #}
        if not (23 in assignedVariableIDs):
        #{
            Main_ErrorPrompt("Gen_GraphLegendTextMaxLength was not found in the config file!\n\nPress any key to retry...")
        
            continue
        #}
        if not (8 in assignedVariableIDs):
        #{
            Prog2_DataDirectory = Gen_WorkingDirectory + "data" + Main_GetPathSeparator()
            
            Main_StatusPrint("Prog2_DataDirectory was not found in the config file, defaulting to \"data\".", 4)
        #}
        if not (9 in assignedVariableIDs):
        #{
            Prog2_GraphViewport[0][0] = None
            
            Main_StatusPrint("Prog2_GraphViewportX1 was not found in the config file, will be adjusted according to the data.", 4)
        #}
        if not (10 in assignedVariableIDs):
        #{
            Prog2_GraphViewport[0][1] = None
            
            Main_StatusPrint("Prog2_GraphViewportX2 was not found in the config file, will be adjusted according to the data.", 4)
        #}
        if not (24 in assignedVariableIDs):
        #{
            Prog2_GraphViewport[1][0] = None
            
            Main_StatusPrint("Prog2_GraphViewportY1 was not found in the config file, will be adjusted according to the data.", 4)
        #}
        if not (25 in assignedVariableIDs):
        #{
            Prog2_GraphViewport[1][1] = None
            
            Main_StatusPrint("Prog2_GraphViewportY2 was not found in the config file, will be adjusted according to the data.", 4)
        #}
        if not (20 in assignedVariableIDs):
        #{
            Main_ErrorPrompt("Prog2_GraphData had no entries in the config file.")

            continue
        #}

        Main_StatusPrint("Successfully gathered parameters from config file.", 1)

        break
    #}
#}

def Main_ImportOtherFiles():
#{
    global data_fx
    global math_fx
    global flattening_fx
    global graphing_fx
    global utils_fx

    directories = [
        Gen_WorkingDirectory + "data", 
        Gen_WorkingDirectory + "math", 
        Gen_WorkingDirectory + "graphing",
        Gen_WorkingDirectory + "utils"
        ]

    Main_CheckDirectories(directories)

    sys.path.append(directories[0])
    sys.path.append(directories[1])
    sys.path.append(directories[2])
    sys.path.append(directories[3])
    sys.path.append(Prog2_DataDirectory)
    
    files = [
        directories[0] + Main_GetPathSeparator() + "data_fx.py", 
        directories[1] + Main_GetPathSeparator() + "math_fx.py", 
        directories[1] + Main_GetPathSeparator() + "flattening_fx.py", 
        directories[2] + Main_GetPathSeparator() + "graphing_fx.py",
        directories[3] + Main_GetPathSeparator() + "utils_fx.py"
        ]

    Main_CheckFiles(files)

    import data_fx
    import math_fx
    import flattening_fx
    import graphing_fx
    import utils_fx
#}

def Main_ResetGlobalVariables():
#{
    global math_fx
    global graphing_fx

    global Gen_WorkingDirectory         #0
    global Gen_GraphConfig              #11 - 19

    global Prog2_DataDirectory          #8
    global Prog2_GraphViewport          #9 - 10, 24 - 25
    global Prog2_GraphData              #20
    global Prog2_GraphDataFlatten       #2
    global Prog2_GraphDataSkips         #26
    global Prog2_GraphDataFits          #27
    global Prog2_GraphDataPeakFinds     #28

    math_fx = None
    graphing_fx = None

    Gen_WorkingDirectory = None
    Gen_GraphConfig = [None, None, None, None, None, None, None, None, None, None, None]

    Prog2_DataDirectory = None
    Prog2_GraphViewport = [[None, None], [None, None]]
    Prog2_GraphData = []
    Prog2_GraphDataFlatten = []
    Prog2_GraphDataSkips = []
    Prog2_GraphDataFits = []
    Prog2_GraphDataPeakFinds = []
#}

def Main_CheckFiles(filePaths):
#{
    for i in range(len(filePaths)):
        Main_CheckFile(filePaths[i])
#}

def Main_CheckFile(filePath):
#{
    file = None

    while (True):
    #{
        try:
        #{
            Main_StatusPrint("Attempting to access file \"" + filePath + "\"...", 0)

            file = open(filePath, "r+")

            break
        #}
        except IOError:
        #{
            Main_ErrorPrompt("Unable to open file!\n\nPress any key to retry...")
        #}
    #}

    file.close()

    Main_StatusPrint("Successfully accessed file.", 1)
#}

def Main_CheckDirectories(directories):
#{
    for i in range(len(directories)):
        Main_CheckDirectory(directories[i])
#}

def Main_CheckDirectory(directory):
#{
    while (True):
    #{
        Main_StatusPrint("Attempting to access directory \"" + directory + "\"...", 0)

        if (os.path.exists(directory) == True):
        #{
            Main_StatusPrint("Successfully accessed directory.", 1)

            break
        #}

        Main_ErrorPrompt("Unable to access directory!\n\nPress any key to retry...")
    #}
#}

def Main_ResizeList(list, size):
#{
    while (size > len(list)):
        list.append([])
#}

def Main_GetPathSeparator():
#{
    if (Main_IsSystemWindows() == True):
        return '/'

    return '\\'
#}

def Main_InsertString(string, insert, pos):
#{
    return (string[: pos] + (insert + string[pos :]))
#}

def Main_ByteString(num, bytes):
#{
    numString = str(num)
    length = len(numString)

    if (length > bytes):
    #{
        numString = ""

        for i in range(bytes):
            numString += "9"

        return numString
    #}

    for i in range(bytes - length):
        numString = "0" + numString;

    return numString
#}

def Main_IsStringNum(string, category):
#}
    if (category == 0):
    #{
        try:
        #{
            int(string)

            return True
        #}
        except ValueError:
        #{
            return False
        #}
    #}
    elif (category == 1):
    #{
        try:
        #{
            float(string)

            return True
        #}
        except ValueError:
        #{
            return False
        #}
    #}
#}

def Main_LoadingStart(loadingText):
#{
    if (Gen_FancyLoading == True):
    #{
        wallLength = 50
        lineLength = 48

        Main_Print(" ")

        wallPrint = ""
        linePrint = "#"

        for i in range(wallLength):
            wallPrint += "#"
        for i in range(lineLength):
            linePrint += " "

        linePrint += "#"

        Main_Print(wallPrint)
        Main_Print(linePrint + "   " + loadingText)
        Main_Print(linePrint)
        Main_Print(wallPrint + "\n")
    #}
#}

def Main_LoadingProgress(current, total, loadingText):
#{
    if (Gen_FancyLoading == True):
    #{
        if (current > total):
            raise ValueError("Current has exceeded total!")

        current = round(current)
        total = round(total)

        Main_OffsetCursorPos(0, -6)

        progress = (current / total)

        if (progress > 1):
            progress = 1

        wallLength = 50
        lineLength = 48
        fullLineLength = round(lineLength * progress)
        emptyLineLength = (lineLength - fullLineLength)

        Main_Print(" ")

        wallPrint = ""
        linePrint = "#"

        for i in range(wallLength):
            wallPrint += "#"
        for i in range(fullLineLength):
            linePrint += "|"
        for i in range(emptyLineLength):
            linePrint += " "

        linePrint += "#"

        Main_Print(wallPrint)
        Main_Print(linePrint + "   " + loadingText)
        Main_Print(linePrint + "   Progress: " + str(current) + " out of " + str(total) + " (" + str(round(progress * 100)) + " %)")
        Main_Print(wallPrint + "\n")
    #}
#}

def Main_LoadingEnd():
#{
    empty = 0
    #if (Gen_FancyLoading == True):
    #{
        #Main_Print("\nLOADING - END\n")
    #}
#}

def Main_StatusPrint(msg, status):
#{
    states = [
        "WORKING ",
        "SUCCESS ",
        "FINISHED",
        "FAILED  ",
        "WARNING "
    ]
    state = ""

    if (status > 4):
        raise ValueError("Unknown status value passed to status print function!")
    else:
        state = states[status]

    Main_Print("STATUS - " + state + ": " + msg)
#}

def Main_ErrorPrompt(msg):
#{
    Main_Input("STATUS - ERROR:\t\t" + msg)

    Main_Print(" ")
#}

def Main_VersionPrints():
#{
    Main_Print("\n------ " + Gen_ProgramName + " v" + str(Gen_ProgramVersion) + " ------")
    Main_Print("-- Author:     Svarun Soda")
    Main_Print("-- Instructor: Nemanja Jovanovic\n")
#}

def Main_SetCursorPos(x, y):
#{
   Main_MoveCursor(x + (y << 16))

   Main_WriteCursorPos(x, y)
#}

def Main_OffsetCursorPos(x, y):
#{
    newX = (Main_GetCursorPos()[0] + x)
    newY = (Main_GetCursorPos()[1] + y)

    Main_MoveCursor(newX + (newY << 16))

    Main_WriteCursorPos(newX, newY)
#}

def Main_MoveCursor(pos):
#{
    ctypes.windll.kernel32.SetConsoleCursorPosition(Gen_GHandle, c_ulong(pos))
#}

def Main_WriteCursorPos(x, y):
#{
    dir = (os.getcwd().replace("\\", Main_GetPathSeparator()) + Main_GetPathSeparator())

    Main_DeleteFile(dir + Gen_CursorPosFileName)
    Main_CreateFile(dir, Gen_CursorPosFileName)

    data = ""

    data += ("curX: " + str(x) + "                    \n")
    data += ("curY: " + str(y) + "                    \n")

    Main_WriteFile(dir, Gen_CursorPosFileName, data)
#}

def Main_GetCursorPos():
#{
    pos = [0, 0]
    cursorFilePath = (os.getcwd().replace("\\", Main_GetPathSeparator()) + Main_GetPathSeparator())

    if (os.path.exists(cursorFilePath + Gen_CursorPosFileName) == True):
    #{
        cursorFileData = Main_ReadFile(cursorFilePath, Gen_CursorPosFileName, 0, -1)
        wordBuff = ""
        waitingValue = -1

        for i in range(len(cursorFileData)):
        #{
            currLine = cursorFileData[i]

            for j in range(len(currLine)):
            #{
                currChar = currLine[j]

                if ((currChar == " ") or (currChar == "\t")):
                #{
                    continue
                #}
                elif (currChar == ":"):
                #{
                    if (wordBuff == "curX"):
                        waitingValue = 0
                    elif (wordBuff == "curY"):
                        waitingValue = 1
                    else:
                        raise ValueError("Unknown identifier encountered in cursor position file!")

                    wordBuff = ""
                #}
                elif (currChar == "\n"):
                #{
                    if (Main_IsStringNum(wordBuff, 0) == True):
                        pos[waitingValue] = int(wordBuff)

                    waitingValue = -1
                    wordBuff = ""
                #}
                else:
                #{
                    wordBuff += currChar
                #}
            #}
        #}
    #}

    if (len(pos) != 2):
        raise ValueError("Unable to acquire current cursor position from cursor position file!")

    return pos
#}

def Main_EnumerateTextLines(text):
#{
    curY = Main_GetCursorPos()[1]
    text = Main_InsertString(text, (str(Main_ByteString(curY, Gen_LineEnumLen)) + ": "), 0)
    idx = (Gen_LineEnumLen + 2)
    localIdx = idx

    while (idx < len(text)):
    #{
        currChar = text[idx]

        if (currChar == "\n"):
        #{
            curY += 1
            text = Main_InsertString(text, (str(Main_ByteString(curY, Gen_LineEnumLen)) + ": "), (idx + 1))

            idx += (Gen_LineEnumLen + 2)
            localIdx = 0
        #}
        else:
        #{
            localIdx += 1
        #}

        if (localIdx >= Gen_MaxCharsPerLine):
            text = Main_InsertString(text, "-\n", idx)

        idx += 1
    #}

    curY += 1
    Main_WriteCursorPos(0, curY)

    return text
#}

def Main_Input(text):
#{
    return input(Main_EnumerateTextLines(text))
#}

def Main_Print(text):
#{
    print(Main_EnumerateTextLines(text))
#}

def Main_CreateDirectory(dirPath):
#{
    if (os.path.exists(dirPath) == False):
        os.makedirs(dirPath)
#}

def Main_WriteFile(filePath, fileName, text):
#{
    fullFilePath = (filePath + fileName)
    
    file = open(fullFilePath, "w")

    file.write(text)

    file.close()
#}

def Main_ReadFile(filePath, fileName, startLine, endLine):
#{
    fullFilePath = (filePath + fileName)
    fullFilePath = fullFilePath.replace("\\", Main_GetPathSeparator())

    idx = startLine

    if (startLine < 0):
        idx = 0

    file = open(fullFilePath, "r+")
    data = []

    while (True):
    #{
        line = file.readline()

        if ((not (line)) or ((endLine >= 0) and (idx >= endLine))):
            break

        data.append(line)

        idx += 1
    #}

    file.close()

    return data
#}

def Main_CreateFile(filePath, fileName):
#{
    fullFilePath = (filePath + fileName)

    if (os.path.isfile(fullFilePath) == True):
        Main_DeleteFile(fullFilePath)

    file = open(fullFilePath, "x")

    file.close()
#}

def Main_DeleteFile(filePath):
#{
    if (os.path.isfile(filePath) == True):
        os.remove(filePath)
#}

def Main_IsSystemWindows():
#{
    if (os.name == "nt"):
        return True

    return False
#}

#### FUNCTIONS END ####

if (__name__ == "__main__"):
    main()