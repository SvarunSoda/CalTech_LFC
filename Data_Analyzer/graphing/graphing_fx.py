#### GRAPHING FUNCTION DEFINITIONS ####

#### BASE IMPORTS ####
import matplotlib.pyplot as plt

#### MY IMPORTS ####
import main_fx
import math_fx
import data_fx
import utils_fx

def Graphing_GraphDataPoints(xData, yData, xViews, yViews, dataLabels, dataSkips, titles, config, scatter, forcedColorIdx, forcedIntegerAxes, displayGraph, saveFileName, txtSaveFileName):
#{
    main_fx.Main_StatusPrint("Attempting to graph data points...", 0)

    if ((len(xData) <= 0) or (len(yData) <= 0)):
        raise ValueError("Attempting to graph some points, but there is no data to graph!")
    if (len(xViews) != 2):
        raise ValueError("Attempting to graph some points, but the size of the X-views array is not 2!")
    if (len(yViews) != 2):
        raise ValueError("Attempting to graph some points, but the size of the Y-views array is not 2!")
    if (len(titles) != 3):
        raise ValueError("Attempting to graph some points, but the size of the titles isn't 3!")

    if ((len(xData) % len(dataLabels)) != 0):
        raise ValueError("Attempting to graph some points, but the sizes of the data and the data labels aren't appropriate!")

    data_fx.Data_CheckSeparatedXYData(xData, yData)

    plt.figure(figsize = (config[0], config[1]), dpi = config[2])
    plt.locator_params(axis = "x", integer = forcedIntegerAxes[0])
    plt.locator_params(axis = "y", integer = forcedIntegerAxes[1])
    plt.title(titles[0])
    plt.xlabel(titles[1])
    plt.ylabel(titles[2])
    plt.xlim(xViews[0], xViews[1])
    plt.ylim(yViews[0], yViews[1])
    plt.grid()

    dataColors = [
        "black",
        "gray",
        "darkred",
        "red",
        "saddlebrown",
        "orange",
        "gold",
        "yellow",
        "darkgreen",
        "lime",
        "cyan",
        "deepskyblue",
        "navy",
        "blue",
        "mediumpurple",
        "darkviolet",
        "springgreen",
        "thistle",
        "hotpink",
        "coral",
        "tan",
        "lightgreen",
        "dodgerblue",
        "indigo"]
    dataLabelIdx = 0
    colorIdx = 0

    if (len(dataLabels) > len(dataColors)):
        raise ValueError("Not enough graph colors!")

    labelsPrinted = []
    labelsPrintedStr = []
    labelsOver = False

    for i in range(len(xData)):
    #{
        if (dataLabelIdx >= len(dataLabels)):
        #{
            dataLabelIdx = 1
            colorIdx = 0
            labelsOver = True
        #}
        else:
        #{
            dataLabelIdx += 1
        #}

        if ((len(dataSkips) > 0) and (dataSkips[i] == 0)):
        #{
            dataLabels[i] = "//"

            continue
        #}

        usedColorIdx = colorIdx

        if (forcedColorIdx != None):
            usedColorIdx = forcedColorIdx

        currLabel = None

        if (scatter == True):
            currLabel = plt.scatter(xData[i], yData[i], label = dataLabels[dataLabelIdx - 1], c = dataColors[dataLabelIdx - 1])
        else:
            currLabel = plt.plot(xData[i], yData[i], marker = "o", markersize = config[3], markeredgecolor = "red", markerfacecolor = "green", label = dataLabels[dataLabelIdx - 1], c = dataColors[usedColorIdx])

        if (labelsOver == False):
        #{
            if (scatter == True):
                labelsPrinted.append(currLabel)
            else:
                labelsPrinted.append(currLabel[0])

            labelsPrintedStr.append(dataLabels[dataLabelIdx - 1])
        #}

        colorIdx += 1
    #}

    idx = 0

    while (idx < len(dataLabels)):
    #{
        idx += 1
        actualIdx = (idx - 1)

        if (dataLabels[actualIdx] == "//"):
        #{
            del dataLabels[actualIdx]
            idx -= 1

            continue
        #}

        #dataLabels[actualIdx] = Graphing_CheckDataLabel(dataLabels[actualIdx], config[9])
    #}

    #for i in range(len(labelsPrintedStr)):
    #    labelsPrintedStr[i] = Graphing_CheckDataLabel(labelsPrintedStr[i], config[9])

    legendSize = config[7]

    if (len(dataLabels) > 0):
        legendSize = (config[7] / len(labelsPrintedStr))

    if (legendSize > config[8]):
        legendSize = config[8]

    plt.legend(handles = labelsPrinted, bbox_to_anchor = (config[5], config[6]), loc = 'upper right', ncol = 1, prop = {"size" : legendSize})
    plt.subplots_adjust(right = config[4])

    main_fx.Main_StatusPrint("Successfully graphed data points.", 1)

    if (len(saveFileName) > 0):
    #{
        saveFileName += config[10]

        main_fx.Main_StatusPrint("Saving graphed data points as \"" + saveFileName + "\"...", 0)

        saveDirPath = utils_fx.Utils_IsolateFilePath(saveFileName)

        main_fx.Main_CreateDirectory(saveDirPath)
        main_fx.Main_CheckDirectory(saveDirPath)
        main_fx.Main_DeleteFile(saveFileName)

        plt.savefig(saveFileName)

        main_fx.Main_StatusPrint("Successfully saved graphed data points.", 1)
    #}

    if (len(txtSaveFileName) > 0):
    #{
        txtSaveFileName += ".txt"

        main_fx.Main_StatusPrint("Saving graphed data points as \"" + txtSaveFileName + "\"...", 0)

        txtSaveDirPath = utils_fx.Utils_IsolateFilePath(txtSaveFileName)
        txtSaveFileName = utils_fx.Utils_IsolateFileName(txtSaveFileName)

        main_fx.Main_CreateDirectory(txtSaveDirPath)
        main_fx.Main_CheckDirectory(txtSaveDirPath)
        main_fx.Main_DeleteFile(txtSaveFileName)

        Graphing_GenerateGraphReportFile(xData, yData, labelsPrintedStr, txtSaveFileName, txtSaveDirPath)

        main_fx.Main_StatusPrint("Successfully saved graphed data points.", 1)
    #}

    if (displayGraph == True):
    #{
        main_fx.Main_StatusPrint("Displaying graphed data points...", 0)

        plt.show()

        main_fx.Main_StatusPrint("Successfully displayed graphed data points.", 1)
    #}

    plt.close()
#}

def Graphing_GenerateGraphReportFile(xData, yData, dataLabels, fileName, reportSavePath):
#{
    data_fx.Data_CheckSeparatedXYData(xData, yData)

    if ((len(xData) % len(dataLabels)) != 0):
        raise ValueError("Data and labels aren't equal!")

    main_fx.Main_CreateDirectory(reportSavePath)
    main_fx.Main_CheckDirectory(reportSavePath)

    main_fx.Main_CreateFile(reportSavePath, fileName)

    data = "---- Graph Data Report File ----\n"
    dataLabelIdx = 0

    for i in range(len(xData)):
    #{
        data += "\n-- Data Set #" + str(i) + " (" + dataLabels[dataLabelIdx] + ") --\n"    

        for j in range(len(xData[i])):
        #{
            data += str(xData[i][j]) + ",\t" + str(yData[i][j]) + "\n"
        #}

        if (dataLabelIdx < (len(dataLabels) - 1)):
            dataLabelIdx += 1
        else:
            dataLabelIdx = 0
    #}

    main_fx.Main_WriteFile(reportSavePath, fileName, data)
#}

def Graphing_CheckDataLabel(dataLabel, maxLength):
#{
    if (len(dataLabel) > maxLength):
    #{
        dataLabel = dataLabel[0 : maxLength]
        dataLabel += "..."
    #}

    return dataLabel
#}