#### MAIN FUNCTION DEFINITIONS ####

#### BASE IMPORTS ####
import sys
import os
import time
import clr

#### MY IMPORTS ####
data_fx = None
math_fx = None
flattening_fx = None
graphing_fx = None
utils_fx = None

#### GLOBAL VARIABLES ####
Gen_ProgramName = "CalTech - LFC Integrated Test #1"
Gen_ProgramVersion = 0.16

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
Gen_ThorWrapperDLL = None                           #26

Prog1_GaussianSigma = None                          #1
Prog1_GaussianPhis = []                             #22
Prog1_GraphViewport = [
    [None, None],                                   #3, 4
    [None, None]                                    #5, 6
    ]
Prog1_GraphAccuracy = None                          #7

Prog2_DataDirectory = None                          #8

#### MAIN PROGRAM FUNCTIONS ####
def main():
#{
    Main_InitProgram()
    Main_VersionPrints()
    
    while (True):
    #{
        Main_ProgramIntegrated()

        time.sleep(3)
    #}

    Main_StatusPrint("---- PROGRAM EXITED ----", 2)
#}

def Main_ProgramIntegrated():
#{
    #STAGE 1:
    #Set XPOW settings

    #STAGE 2:
    #Iterate through 0V - 20V on XPOW
    #Load & save spectrum for each iteration from OSA

    #STAGE 3:
    #Take differences between 0V & all others
    #Smooth all difference plots

    #STAGE 4:
    #Fit & plot 20 Gaussians to all difference plots

    #STAGE 5:
    #Plot & save V vs. A plots for all difference plots

    #STAGE 6:
    #Correct Gaussians for next iteration
    #Send commands to XPOW

    dummyData = [
        ["Ch_14_V_00_A_50.txt"],
        ["Ch_14_V_01_A_50.txt"],
        ["Ch_14_V_02_A_50.txt"],
        ["Ch_14_V_03_A_50.txt"],
        ["Ch_14_V_04_A_50.txt"],
        ["Ch_14_V_05_A_50.txt"],
        ["Ch_14_V_06_A_50.txt"],
        ["Ch_14_V_07_A_50.txt"],
        ["Ch_14_V_08_A_50.txt"],
        ["Ch_14_V_09_A_50.txt"],
        ["Ch_14_V_10_A_50.txt"],
        ["Ch_14_V_11_A_50.txt"],
        ["Ch_14_V_12_A_50.txt"],
        ["Ch_14_V_13_A_50.txt"],
        ["Ch_14_V_14_A_50.txt"],
        ["Ch_14_V_15_A_50.txt"],
        ["Ch_14_V_16_A_50.txt"],
        ["Ch_14_V_17_A_50.txt"],
        ["Ch_14_V_18_A_50.txt"],
        ["Ch_14_V_19_A_50.txt"],
        ["Ch_14_V_20_A_50.txt"]
        ]

    for channelIdx in range(2):
    #{
        diffDataY = []

        peakFindDataX = []
        peakFindDataY = []

        for voltageIdx in range(18):
        #{
            #STAGE 1:
            #Set XPOW settings
            #TODO

            #STAGE 2:
            #Iterate through 0V - 20V on XPOW
            #Load & save spectrum for each iteration from OSA
            currDataNames = dummyData[voltageIdx]
            currFlatteningData = [[2, 0.01, 1, 8.494, 0, 1]]
            currDataSkips = [1]
            currDataFits = [1]

            data = data_fx.Data_LoadDataFromFiles(Prog2_DataDirectory, 
                                                  currDataNames, 
                                                  [], 
                                                  currFlatteningData, 
                                                  currDataSkips)

            xData = []
            yData = []
    
            data_fx.Data_SeparateXYData(data, xData, yData)

            if (voltageIdx == 0):
            #{
                for j in range(len(yData[0])):
                    diffDataY.append(yData[0][j])

                continue
            #}

            #STAGE 3:
            #Take differences between 0V & all others
            #Smooth all difference plots
            for j in range(len(yData[0])):
                yData[0][j] = yData[0][j] - diffDataY[j]

            flattening_fx.Math_FlattenDatas(xData, 
                                            yData, 
                                            [Prog1_GraphViewport[0][0], Prog1_GraphViewport[0][1]], 
                                            currFlatteningData)

            peakFindDataX.append(xData[0])
            peakFindDataY.append(yData[0])
        #}
        
        if (len(peakFindDataX) > 0):
        #{
            #STAGE 4:
            #Fit & plot 20 Gaussians to all difference plots
            gaussianSigmas = []
            gaussianPhis = []
            gaussianAmplitudes = []

            for j in range(len(Prog1_GaussianPhis)):
            #{
                gaussianSigmas.append(Prog1_GaussianSigma)
                gaussianPhis.append(Prog1_GaussianPhis[j])
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

                dataLabels = ["TEST"]

                mus = data_fx.Data_FitGaussiansToDatas(xData, 
                                                 yData, 
                                                 gaussianSigmas, 
                                                 gaussianPhis, 
                                                 1300, 1900, 
                                                 0, 
                                                 gaussianAmplitudes, 
                                                 1420, 
                                                 dataLabels, 
                                                 [], [], [], 
                                                 True,
                                                 voltageIdx, 
                                                 Prog2_DataDirectory + "reports" + Main_GetPathSeparator(), "GaussianFit_Report_")

                xViews = [utils_fx.Utils_MinOfLists(xData), utils_fx.Utils_MaxOfLists(xData)]
                yViews = [(utils_fx.Utils_MinOfLists(yData) - 10), (utils_fx.Utils_MaxOfLists(yData) + 10)]

                if (Prog1_GraphViewport[0][0] != None):
                    xViews[0] = Prog1_GraphViewport[0][0]
                if (Prog1_GraphViewport[0][1] != None):
                    xViews[1] = Prog1_GraphViewport[0][1]
                if (Prog1_GraphViewport[1][0] != None):
                    yViews[0] = Prog1_GraphViewport[1][0]
                if (Prog1_GraphViewport[1][1] != None):
                    yViews[1] = Prog1_GraphViewport[1][1]

                graphing_fx.Graphing_GraphDataPoints(xData, yData, 
                                                    xViews, 
                                                    yViews, 
                                                    dataLabels,
                                                    currDataSkips,
                                                    [Gen_ProgramName + " v" + str(Gen_ProgramVersion), "Spectrum (nm)", "Level (db)"],
                                                    Gen_GraphConfig, 
                                                    False,
                                                    None, 
                                                    [False, False],
                                                    False, Prog2_DataDirectory + "plots" + Main_GetPathSeparator() + "Plot_" + str(voltageIdx), "")

                del peakFindDatasX[len(peakFindDatasX) - 1][0]
            #}

            #STAGE 5:
            #Plot & save V vs. A plots for all difference plots
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
                                                    False, Prog2_DataDirectory + "plots" + Main_GetPathSeparator() + "AmplitudeVoltage_Plot_" + str(graphIdx), Prog2_DataDirectory + "plots" + Main_GetPathSeparator() + "AmplitudeVoltage_Plot_" + str(graphIdx))

                idx += iterations
                graphIdx += 1
            #}

            amplitudeDataSkips = []

            for j in range(len(amplitudeDataX)):
                amplitudeDataSkips.append(1)

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
                                                False, Prog2_DataDirectory + "plots" + Main_GetPathSeparator() + "AmplitudeVoltage_Plot_All", Prog2_DataDirectory + "plots" + Main_GetPathSeparator() + "AmplitudeVoltage_Plot_All")
        #}

        #STAGE 6:
        #Correct Gaussians for next iteration
        #Send commands to XPOW
        #TODO
    #}
#}

#### SUPPORTING FUNCTIONS ####

def Main_InitProgram():
#{
    Main_AssignGlobalVariablesFromFile("config.txt")
    Main_CheckDirectory(Gen_WorkingDirectory)
    Main_CheckDirectory(Gen_ThorWrapperDLL)
    Main_ImportOtherFiles()
#}

def Main_AssignGlobalVariablesFromFile(fileName):
#{
    while (True):
    #{
        Main_ResetGlobalVariables()

        global Gen_WorkingDirectory
        global Gen_ThorWrapperDLL
        global Gen_GraphConfig

        global Prog1_GaussianSigma
        global Prog1_GaussianPhis
        global Prog1_GraphViewport
        global Prog1_GraphAccuracy

        global Prog2_DataDirectory

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

                if (currChar == '\n') or (currChar == '\t'):
                #{
                    foundSpace = True
                #}
                elif (currChar == ' '):
                #{
                    if (len(wordBuff) == 0):
                    #{
                        foundSpace = True
                    #}
                    else:
                    #{
                        wordBuff += currChar
                    #}
                #}
                elif (currChar == '"') or (currChar == '\''):
                #{
                    continue
                #}
                elif (currChar == '#'):
                #{
                    break
                #}
                else:
                #{
                    wordBuff += currChar
                #}

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
                    elif (wordBuff == "Gen_ThorWrapperDLL"):    
                        foundID = 26
                    elif (wordBuff == "Prog1_GaussianSigma"):    
                        foundID = 1
                    elif (wordBuff == "Prog1_GraphViewportX1"): 
                        foundID = 3
                    elif (wordBuff == "Prog1_GraphViewportX2"):
                        foundID = 4
                    elif (wordBuff == "Prog1_GraphViewportY1"):
                        foundID = 5
                    elif (wordBuff == "Prog1_GraphViewportY2"):
                        foundID = 6
                    elif (wordBuff == "Prog1_GraphAccuracy"):
                        foundID = 7
                    elif (wordBuff == "Prog1_GaussianPhis"):
                        foundID = 22
                    elif (wordBuff == "Prog2_DataDirectory"):
                        foundID = 8

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
                                Gen_WorkingDirectory = Main_RemoveSpacePaddingFromString(value)
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
                            if (lastVariableID == 26):
                            #{
                                Gen_ThorWrapperDLL = Main_RemoveSpacePaddingFromString(value)
                            #}
                            elif (lastVariableID == 1):
                            #{
                                if (Main_IsStringNum(value, 1) == False):
                                    raise ValueError("Prog1_GaussianSigma was expecting a numerical value!")

                                Prog1_GaussianSigma = float(value)
                            #}
                            elif (lastVariableID == 3):
                            #{
                                if (Main_IsStringNum(value, 1) == False):
                                    raise ValueError("Prog1_GraphViewport[0][0] was expecting a numerical value!")

                                Prog1_GraphViewport[0][0] = float(value)
                            #}
                            elif (lastVariableID == 4):
                            #{
                                if (Main_IsStringNum(value, 1) == False):
                                    raise ValueError("Prog1_GraphViewport[0][1] was expecting a numerical value!")

                                Prog1_GraphViewport[0][1] = float(value)
                            #}
                            elif (lastVariableID == 5):
                            #{
                                if (Main_IsStringNum(value, 1) == False):
                                    raise ValueError("Prog1_GraphViewport[1][0] was expecting a numerical value!")

                                Prog1_GraphViewport[1][0] = float(value)
                            #}
                            elif (lastVariableID == 6):
                            #{
                                if (Main_IsStringNum(value, 1) == False):
                                    raise ValueError("Prog1_GraphViewport[1][1] was expecting a numerical value!")

                                Prog1_GraphViewport[1][1] = float(value)
                            #}
                            elif (lastVariableID == 7):
                            #{
                                if (Main_IsStringNum(value, 0) == False):
                                    raise ValueError("Prog1_GraphAccuracy was expecting a numerical value!")

                                Prog1_GraphAccuracy = int(value)
                            #}
                            elif (lastVariableID == 22):
                            #{
                                if (Main_IsStringNum(value, 1) == False):
                                    raise ValueError("Prog1_GaussianPhis was expecting a numerical value!")

                                Prog1_GaussianPhis.append(float(value))
                            #}
                            elif (lastVariableID == 8):
                            #{
                                Prog2_DataDirectory = Main_RemoveSpacePaddingFromString(value)
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
        if not (26 in assignedVariableIDs):
        #{
            Main_ErrorPrompt("Gen_ThorWrapperDLL was not found in the config file!\n\nPress any key to retry...")
        
            continue
        #}
        if not (1 in assignedVariableIDs):
        #{
            Main_ErrorPrompt("Prog1_GaussianSigma was not found in the config file!\n\nPress any key to retry...")

            continue
        #}
        if not (3 in assignedVariableIDs):
        #{
            Main_ErrorPrompt("Prog1_GraphViewportX1 was not found in the config file!\n\nPress any key to retry...")
        
            continue
        #}
        if not (4 in assignedVariableIDs):
        #{
            Main_ErrorPrompt("Prog1_GraphViewportX2 was not found in the config file!\n\nPress any key to retry...")
        
            continue
        #}
        if not (5 in assignedVariableIDs):
        #{
            Main_ErrorPrompt("Prog1_GraphViewportY1 was not found in the config file!\n\nPress any key to retry...")
        
            continue
        #}
        if not (6 in assignedVariableIDs):
        #{
            Main_ErrorPrompt("Prog1_GraphViewportY2 was not found in the config file!\n\nPress any key to retry...")
        
            continue
        #}
        if not (7 in assignedVariableIDs):
        #{
            Main_ErrorPrompt("Prog1_GraphAccuracy was not found in the config file!\n\nPress any key to retry...")
        
            continue
        #}
        if not (22 in assignedVariableIDs):
        #{
            Main_ErrorPrompt("Prog1_GaussianPhis was not found in the config file!\n\nPress any key to retry...")
        
            continue
        #}
        if not (8 in assignedVariableIDs):
        #{
            Prog2_DataDirectory = Gen_WorkingDirectory + "data" + Main_GetPathSeparator()
            
            Main_StatusPrint("Prog2_DataDirectory was not found in the config file, defaulting to \"data\".", 4)
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

    clr.AddReference(Gen_ThorWrapperDLL)
    
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
    global data_fx
    global math_fx
    global flattening_fx
    global graphing_fx
    global utils_fx

    global Gen_WorkingDirectory         #0
    global Gen_GraphConfig              #11 - 19
    global Gen_ThorWrapperDLL     #26

    global Prog1_GaussianSigma          #1
    global Prog1_GaussianPhis           #22
    global Prog1_GraphViewport          #3 - 6
    global Prog1_GraphAccuracy          #7

    global Prog2_DataDirectory          #8
    global Prog2_GraphData              #20

    data_fx = None
    math_fx = None
    flattening_fx = None
    graphing_fx = None
    utils_fx = None

    Gen_WorkingDirectory = None
    Gen_GraphConfig = [None, None, None, None, None, None, None, None, None, None, None]
    Gen_ThorWrapperDLL = None

    Prog1_GaussianSigma = None
    Prog1_GaussianPhis = []
    Prog1_GraphViewport = [[None, None], [None, None]]
    Prog1_GraphAccuracy = None

    Prog2_DataDirectory = None
    Prog2_GraphData = []
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

def Main_RemoveSpacePaddingFromString(string):
#{
    startIdx = 0
    endIdx = len(string) - 1

    while (startIdx < len(string)):
    #{
        currChar = string[startIdx]

        if (currChar != " ") and (currChar != "\t"):
            break

        startIdx += 1
    #}
    while (endIdx >= 0):
    #{
        currChar = string[endIdx]

        if (currChar != " ") and (currChar != "\t"):
            break

        endIdx -= 1
    #}

    return string[startIdx : (endIdx + 1)]
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

def Main_Input(text):
#{
    return input(text)
#}

def Main_Print(text):
#{
    print(text)
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