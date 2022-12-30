#### DATA FUNCTION DEFINITIONS ####

#### MY IMPORTS ####
import main_fx
import math_fx
import data_fx
import utils_fx
import numpy as np
#from decimal import *

def Data_IdentifyHighPeak(peakFindDataX, peakFindDataY, dataEdges, intersectionTolerance, fileName, reportSavePath):
#{
    foundPointsX = []
    foundPointsY = []

    for i in range(len(peakFindDataX)):
    #{
        currPeakFindDataX = peakFindDataX[i]
        currPeakFindDataY = peakFindDataY[i]

        if (len(currPeakFindDataX) > 2):
        #{
            foundPointsX.append([])
            foundPointsY.append([])

            peaks = []
            trackedPointsX = []
            trackedPointsY = []
            lastSlopeSign = 0
            #idx = 0
            #endIdx = (len(currPeakFindDataX) - 1)
            idx = utils_fx.Utils_FindInList(currPeakFindDataX, math_fx.Math_GetClosestNum(dataEdges[0], currPeakFindDataX))
            endIdx = utils_fx.Utils_FindInList(currPeakFindDataX, math_fx.Math_GetClosestNum(dataEdges[1], currPeakFindDataX))

            while (idx < endIdx):
            #{
                currX = currPeakFindDataX[idx]
                currY = currPeakFindDataY[idx]
                nextX = currPeakFindDataX[idx + 1]
                nextY = currPeakFindDataY[idx + 1]

                currPoints = [
                    0,
                    currY,
                    1,
                    nextY
                    ]

                currSlope = math_fx.Math_InterpolatePointsLinear(currPoints)[1]
                canSaveCurrentPoints = False

                if (idx > 0):
                #{
                    if (currSlope > 0):
                    #{
                        if (lastSlopeSign == -1):
                            canSaveCurrentPoints = True
                    #}
                    elif (currSlope == 0):
                    #{
                        if (lastSlopeSign == -1):
                            canSaveCurrentPoints = True
                    #}

                #}
                
                if (canSaveCurrentPoints == True):
                #{
                    foundPointsX[i].append(trackedPointsX)
                    foundPointsY[i].append(trackedPointsY)

                    trackedPointsX = []
                    trackedPointsY = []
                #}

                trackedPointsX.append(currX)
                trackedPointsY.append(currY)

                lastSlopeSign = 0

                if (currSlope < 0):
                    lastSlopeSign = -1
                elif (currSlope > 0):
                    lastSlopeSign = 1

                idx += 1
            #}

            foundPointsX[i].append(trackedPointsX)
            foundPointsY[i].append(trackedPointsY)

            trackedPointsX = []
            trackedPointsY = []
        #}
    #}

    if (len(foundPointsX) > 0):
    #{
        largestFoundPointsX = []
        largestFoundPointsY = []

        for i in range(len(foundPointsX)):
        #{
            currFoundPointsX = foundPointsX[i]
            currFoundPointsY = foundPointsY[i]
            largestDiff = 0
            largestDiffIdx = 0

            for j in range(len(currFoundPointsX)):
            #{
                currLocalFoundPointsY = currFoundPointsY[j]
                currLocalFoundPointsMax = max(currLocalFoundPointsY)
                currLocalFoundPointsMin = min(currLocalFoundPointsY)

                currDiff = (currLocalFoundPointsMax - currLocalFoundPointsMin)

                if (currDiff > largestDiff):
                #{
                    largestDiff = currDiff
                    largestDiffIdx = j
                #}
            #}

            largestFoundPointsX.append(currFoundPointsX[largestDiffIdx])
            largestFoundPointsY.append(currFoundPointsY[largestDiffIdx])
        #}

        intersectionsX = []

        for i in range(len(largestFoundPointsX)):
        #{
            currLargestFoundPointsX = largestFoundPointsX[i]
            currIntersectionsX = []
            idx = 0

            while (idx < len(largestFoundPointsX)):
            #{
                if (idx != i):
                #{
                    currSearchLargestFoundPointsX = largestFoundPointsX[idx]
                    currIntersectionX = []

                    for j in range(len(currLargestFoundPointsX)):
                    #{
                        currSearchingX = currLargestFoundPointsX[j]
                        currFoundXIdx = utils_fx.Utils_FindInList(currSearchLargestFoundPointsX, currSearchingX)

                        if (currFoundXIdx != -1):
                            currIntersectionX.append(currSearchingX)
                    #}

                    currIntersectionsX.append(currIntersectionX)
                #}

                idx += 1
            #}

            intersectionsX.append(currIntersectionsX)
        #}
        
        if (len(intersectionsX) == 0):
            Data_GenerateHighPeakReportFile([], fileName, reportSavePath)

        finalIntersectionsX = []
        outerNonIntersectionTolerance = intersectionTolerance
        innerNonIntersectionTolerance = intersectionTolerance
        outerNonIntersections = 0

        for i in range(len(intersectionsX)):
        #{
            currIntersectionsX = intersectionsX[i]
            innerNonIntersections = 0
            currFinalXIntersects = []
            intersecting = True

            for j in range(len(currIntersectionsX)):
            #{
                currIntersectionX = currIntersectionsX[j]

                if (len(currIntersectionX) == 0):
                #{
                    innerNonIntersections += 1

                    if (innerNonIntersections >= innerNonIntersectionTolerance):
                    #{
                        intersecting = False

                        break
                    #}
                #}
                else:
                #{
                    currFinalXIntersects.append(currIntersectionX)
                #}
            #}

            if (intersecting == False):
            #{
                outerNonIntersections += 1

                if (outerNonIntersections >= outerNonIntersectionTolerance):
                     break
            #}
            else:
            #{
                currFinalInteresectX = utils_fx.Utils_IntersectLists(currFinalXIntersects, 0, True)

                finalIntersectionsX.append(currFinalInteresectX)
            #}
        #}

        if (len(finalIntersectionsX) == 0):
            Data_GenerateHighPeakReportFile([], fileName, reportSavePath)

        finalIntersectionsXMaxSize = utils_fx.Utils_MaxSizeOfLists(finalIntersectionsX)
        finalIntersectionsXMinSize = utils_fx.Utils_MinSizeOfLists(finalIntersectionsX)
        finalIntersectionsXClipSize = math_fx.Math_ListAverage([finalIntersectionsXMaxSize, finalIntersectionsXMinSize])
        idx = 0

        while (idx < len(finalIntersectionsX)):
        #{
            if (len(finalIntersectionsX[idx]) <= finalIntersectionsXClipSize):
            #{
                del finalIntersectionsX[idx]

                idx -= 1
            #}

            idx += 1
        #}

        #finalIntersectionsXOccurenceList = utils_fx.Utils_GenerateOccurenceList(finalIntersectionsX)
        #finalIntersectionsXMaxOccurence = max(finalIntersectionsXOccurenceList[1])
        #
        #for i in range(len(finalIntersectionsX)):
        ##{
        #    currFinalIntersectionX = finalIntersectionsX[i]
        #    j = 0
        #
        #    while (j < len(currFinalIntersectionX)):
        #    #{
        #        currX = currFinalIntersectionX[j]
        #        currXOccurence = finalIntersectionsXOccurenceList[1][utils_fx.Utils_FindInList(finalIntersectionsXOccurenceList[0], currX)]
        #
        #        if (currXOccurence <= (finalIntersectionsXMaxOccurence / 2)):
        #        #{
        #            del finalIntersectionsX[i][j]
        #
        #            j -= 1
        #        #}
        #
        #        j += 1
        #    #}
        ##}

        finalIntersectionX = utils_fx.Utils_IntersectLists(finalIntersectionsX, 0, True)
        #finalIntersectionX = sorted(utils_fx.Utils_UnionLists(finalIntersectionsX))
        finalIntersectionYs = []

        for i in range(len(foundPointsX)):
        #{
            currFoundPointsX = foundPointsX[i]
            currFoundPointsY = foundPointsY[i]
            currFinalIntersetcionYs = []

            for j in range(len(currFoundPointsX)):
            #{
                currLocalFoundPointsX = currFoundPointsX[j]
                currLocalFoundPointsY = currFoundPointsY[j]

                for k in range(len(currLocalFoundPointsX)):
                #{
                    currPointX = currLocalFoundPointsX[k]
                    currPointY = currLocalFoundPointsY[k]

                    if (utils_fx.Utils_FindInList(finalIntersectionX, currPointX) != -1):
                    #{
                        if (utils_fx.Utils_FindInList(currFinalIntersetcionYs, currPointY) != -1):
                            raise ValueError("Double Y insertion during final intersection!")

                        currFinalIntersetcionYs.append(currPointY)
                    #}
                #}
            #}

            finalIntersectionYs.append(currFinalIntersetcionYs)
        #}

        finalSineParams = []

        for i in range(len(finalIntersectionYs)):
        #{
            currFinalIntersectionY = finalIntersectionYs[i]

            if (len(currFinalIntersectionY) != len(finalIntersectionX)):
            #{
                finalSineParams.append([])

                continue
            #}

            finalSineParams.append(math_fx.Math_FitSineToData(finalIntersectionX, currFinalIntersectionY))
        #}

        Data_GenerateHighPeakReportFile(finalIntersectionX, finalSineParams, fileName, reportSavePath)
    #}
#}

def Data_GenerateHighPeakReportFile(peakSpectrumX, sineParams, fileName, reportSavePath):
#{
    main_fx.Main_CreateDirectory(reportSavePath)
    main_fx.Main_CheckDirectory(reportSavePath)

    main_fx.Main_CreateFile(reportSavePath, fileName)

    data = "---- High Peak Report File ----\n\nPeak Likely at X values: {"
    data += (str(round(peakSpectrumX[0], 3)) + " - " + str(round(peakSpectrumX[len(peakSpectrumX) - 1], 3)))
    data += "}\n\nFinal Sine Params:\n"

    for i in range(len(sineParams)):
    #{
        data += ("\nDataset #" + str(i))

        currSineParams = sineParams[i]

        if (len(currSineParams) == 0):
        #{
            data += " -\tUnable to compute a Sine function!"

            continue
        #}
            
        data += (" -\tAmplitude: " + str(round(currSineParams[0], 3)) + "\tStretch: " + str(round(currSineParams[1], 3)) + "\tHorizontal Shift: " + str(round(currSineParams[2], 3)) + "\tVertical Shift: " + str(round(currSineParams[3], 3)))
    #}

    main_fx.Main_WriteFile(reportSavePath, fileName, data)
#}

def Data_FitGaussiansToDatas(xData, yData, sigmas, phis, xStart, xEnd, iterations, amplitudes, xAxisStart, dataLabels, dataFlattening, dataSkips, dataFits, calculateSum, reportNum, reportSavePath, reportFileName):
#{
    Data_CheckSeparatedXYData(xData, yData)

    main_fx.Main_StatusPrint("Attemtping to fit Gaussians to some data...", 0)    

    datasNum = len(xData)
    retMus = []
    idx = 0

    while (idx < datasNum):
    #{
        idx += 1

        if ((len(dataFits) > 0) and (dataFits[(idx - 1)] == 0)):
            continue

        currIdx = (idx - 1)

        currXData = xData[currIdx]
        currYData = yData[currIdx]
        #currDaraLabel = dataLabels[currIdx]
        currFlatteningData = None
        currDataSkip = None

        if (len(dataFlattening) > 0):
            currFlatteningData = dataFlattening[currIdx]
        if (len(dataSkips) > 0):
            currDataSkip = dataSkips[currIdx]

        mus = []

        gaussianData = math_fx.Math_GenerateGaussianData(sigmas, 
                                                         phis, 
                                                         xStart, 
                                                         xEnd, 
                                                         iterations, 
                                                         amplitudes, 
                                                         xAxisStart, 
                                                         currXData, 
                                                         currYData, 
                                                         mus, 
                                                         calculateSum, 
                                                         False)

        if ((reportSavePath != "") and (reportFileName != "")):
            Data_GenerateFitReportFile(sigmas, phis, amplitudes, mus, currIdx, (reportFileName + str(reportNum) + "_" + str(currIdx) + ".txt"), reportNum, reportSavePath)

        retMus.append(mus)

        gaussianXData = []
        gaussianYData = []

        data_fx.Data_SeparateXYData(gaussianData, gaussianXData, gaussianYData)

        Data_CheckSeparatedXYData(gaussianXData, gaussianYData)

        for j in range(len(gaussianXData)):
        #{
            xData.insert(j, gaussianXData[j])
            yData.insert(j, gaussianYData[j])

            if (len(dataFlattening) > 0):
                dataFlattening.insert(j, [-1])
            if (len(dataSkips) > 0):
                dataSkips.insert(j, 1)

            if ((calculateSum == True) and (j == (len(gaussianXData) - 1))):
                dataLabels.insert(j, "Gaussian Sum")
            else:
                dataLabels.insert(j, "Gaussian #" + str(j) + " (a = " + str(round(amplitudes[j], 3)) + ")")
        #}
    #}

    Data_CheckSeparatedXYData(xData, yData)

    main_fx.Main_StatusPrint("Successfully fitted Gaussians to some data.", 1)

    return retMus
#}

def Data_GenerateFitReportFile(sigmas, phis, amplitudes, mus, fileNum, fileName, reportNum, reportSavePath):
#{
    if ((len(sigmas) != len(phis)) or (len(sigmas) != len(amplitudes)) or (len(sigmas) != len(mus))):
        raise ValueError("Attempting to generate a fit report file, but some of the Gaussian datas are not the same size!")

    main_fx.Main_CreateDirectory(reportSavePath)
    main_fx.Main_CheckDirectory(reportSavePath)

    main_fx.Main_CreateFile(reportSavePath, fileName)

    data = ("---- Gaussian Fit #" + str(reportNum) + " Report File #" + str(fileNum) + " ----\n")

    for i in range(len(sigmas)):
        data += ("\n- Gaussian #" + str(main_fx.Main_ByteString(i, 3)) + " -\t\tSigma: " + str(round(sigmas[i], 3)) + "\tPhi: " + str(round(phis[i], 3)) + "\tMu: " + str(round(mus[i], 0)) + "\tAmplitude: " + str(round(amplitudes[i], 3)))

    main_fx.Main_WriteFile(reportSavePath, fileName, data)
#}

def Data_PerformOperatorsOnData(xData, yData, dataNames, dataLabels, dataFlattening, dataSkips):
#{
    Data_CheckSeparatedXYData(xData, yData)

    dataInsertOffset = 0

    for i in range(len(dataNames)):
    #{
        currDataName = dataNames[i]
        operatorStartIdx = currDataName.find("<")
        operatorEndIdx = currDataName.find(">")

        if (operatorStartIdx != -1) and (operatorEndIdx != -1):
        #{
            operator = currDataName[(operatorStartIdx + 1) : operatorEndIdx]
            firstOperatorArg = utils_fx.Utils_RemoveFileNameExt(currDataName[0 : operatorStartIdx])
            secondOperatorArg = utils_fx.Utils_RemoveFileNameExt(currDataName[(operatorEndIdx + 1) : len(currDataName)])
            firstOperatorArgIdx = utils_fx.Utils_FindInList(dataLabels, firstOperatorArg)
            secondOperatorArgIdx = utils_fx.Utils_FindInList(dataLabels, secondOperatorArg)

            if (firstOperatorArgIdx == -1):
                raise ValueError("First argument of a data operator is not found in the data!")
            if (secondOperatorArgIdx == -1):
                raise ValueError("Second argument of a data operator is not found in the data!")

            if (operator == "-"):
                data_fx.Data_DiffXYDatas(xData, yData, firstOperatorArgIdx, [secondOperatorArgIdx], dataLabels)
            else:
                raise ValueError("This type of data operator has not been implemented yet!")

            dataSkips[1].append(dataSkips[0][i])
            dataFlattening[1].append(dataFlattening[0][i])

            dataInsertOffset += 1
        #}
        else:
        #{
            dataSkips[1][i - dataInsertOffset] = dataSkips[0][i]
            dataFlattening[1][i - dataInsertOffset] = dataFlattening[0][i]
        #}
    #}

    Data_CheckSeparatedXYData(xData, yData)
#}

def Data_DiffXYDatas(xData, yData, diffDataIdx, diffedDataIndices, dataLabels):
#{
    if (len(diffedDataIndices) == 0):
        raise ValueError("Attempting to diff no data!")

    main_fx.Main_StatusPrint("Attemtping to diff some data...", 0)

    Data_CheckSeparatedXYData(xData, yData)

    idx = -1
    dataNum = len(xData)

    while (idx < (dataNum - 1)):
    #{
        idx += 1

        if (idx == diffDataIdx) or not (idx in diffedDataIndices):
            continue
        
        diffedYData = []
    
        Data_DiffXYData(xData[idx], yData[idx], yData[diffDataIdx], diffedYData)
    
        xData.append(xData[idx])
        yData.append(diffedYData)
        dataLabels.append("(" + dataLabels[diffDataIdx] + " - " + dataLabels[idx] + ")")
    #}

    Data_CheckSeparatedXYData(xData, yData)

    main_fx.Main_StatusPrint("Successfully diffed the data.", 1)
#}

def Data_DiffXYData(xData, yData1, yData2, yDiffData):
#{
    if (len(xData) != len(yData1)):
        raise ValueError("Attempting to diff data, but the sizes of the X and Y1 data points disconnected during separation!")
    if (len(xData) != len(yData2)):
        raise ValueError("Attempting to diff data, but the sizes of the X and Y2 data points disconnected during separation!")

    for i in range(len(xData)):
        yDiffData.append(yData2[i] - yData1[i])
#}

def Data_SeparateXYData(data, xData, yData):
#{
    xLast = 0
    dataNum = 0
    dataIdx = 0
    tracking = True

    for i in range(len(data)):
    #{
        currData = data[i]

        if ((i % 2) == 0):
        #{
            if ((tracking == True) and ((i == 0) or (currData == xLast))):
            #{
                xData.append([])
                yData.append([])

                dataNum += 1
                xLast = currData
            #}
            elif (tracking == True):
            #{
                dataIdx = 0
                tracking = False
            #}

            xData[dataIdx].append(currData)
        #}
        else:
        #{
            yData[dataIdx].append(currData)

            if (tracking == True) or (dataIdx < (dataNum - 1)):
                dataIdx += 1
            else:
                dataIdx = 0
        #}
    #}

    utils_fx.Utils_CheckEqualListSizes(xData)
    utils_fx.Utils_CheckEqualListSizes(yData)
    data_fx.Data_CheckSeparatedXYData(xData, yData)
#}

def Data_CombineXYData(xData, yData):
#{
    Data_CheckSeparatedXYData(xData, yData)

    data = []
    idx = 0

    while (True):
    #{
        datasLeft = len(xData)

        for i in range(len(xData)):
        #{
            currDataX = xData[i]
            currDataY = yData[i]

            if (len(currDataX) > idx):
            #{
                data.append(currDataX[idx])
                data.append(currDataY[idx])
            #}
            else:
            #{
                datasLeft -= 1
            #}
        #}

        if (datasLeft < 0):
            raise ValueError("Data tracker became negative while attempting to combine data!")
        elif (datasLeft == 0):
            break

        idx += 1
    #}

    return data
#}

def Data_CheckSeparatedXYData(xData, yData):
#{
    if (len(xData) != len(yData)):
        raise ValueError("Attempting to separate data, but the sizes of the X and Y data points disconnected during separation!")

    for i in range(len(xData)):
        if (len(xData[i]) != len(yData[i])):
            raise ValueError("Attempting to separate data, but the sizes of one of the X and Y local data points disconnected during separation!")
#}

def Data_FillFakeData(data, dataNum, fakeInsert):
#{
    if (len(data) == 0):
        raise ValueError("Attempting to fill fake data into no data!")
    if ((len(data) % 2) != 0):
        raise ValueError("Attempting to fill fake data into odd data!")

    idx = 0
    xLast = data[0]
    tracker = 0
    emptyTracker = 0

    while (idx < len(data)):
    #{
        if (idx == (len(data) - 4)):
            bruh = 0

        xCurr = data[idx]
        yCurr = data[idx + 1]

        if (tracker == 0):
            xLast = xCurr

        if (tracker < (dataNum - 1)):
        #{
            if (xCurr != xLast):
                emptyTracker += 1

            tracker += 1

            if (idx == (len(data) - 2)):
            #{
                for i in range(dataNum - tracker):
                #{
                    data.append(xLast)
                    data.append(fakeInsert)
                #}
            #}
        #}
        else:
        #{
            if (xCurr != xLast):
                emptyTracker += 1

            for i in range(emptyTracker):
            #{
                data.insert(idx, fakeInsert)
                data.insert(idx, xLast)
            #}

            tracker = 0
            emptyTracker = 0
        #}

        idx += 2
    #}
#}

def Data_LoadDataFromFiles(dataDirectory, dataNames, dataLabels, flattenData, dataSkips):
#{
    main_fx.Main_CheckDirectory(dataDirectory)

    rawData = []

    for i in range(len(dataNames)):
    #{
        currFileNames = []
        currFileDesc = dataNames[i]

        if (currFileDesc.find("<") != -1) or (currFileDesc.find(">") != -1):
            continue
        
        starIdxPos = currFileDesc.find("*.")

        if (starIdxPos != -1):
        #{
            searchFileName = currFileDesc[0 : starIdxPos]
            searchExt = currFileDesc[(starIdxPos + 1) : len(currFileDesc)]
            currFlattenData = flattenData[i]
            currSkipData = dataSkips[i]
            
            del dataNames[i]
            del flattenData[i]
            del dataSkips[i]

            currSearchFiles = [f for f in os.listdir(dataDirectory) if os.path.isfile(os.path.join(dataDirectory, f))]

            if (len(currSearchFiles) == 0):
                raise ValueError("Not found requested search files!")

            for j in range(len(currSearchFiles)):
            #{
                currSearchFileName = currSearchFiles[j]
                currSearchFileExt = currSearchFileName[(len(currSearchFileName) - 4) : len(currSearchFileName)]

                if ((len(searchFileName) > 0) and (currSearchFileName.find(searchFileName) != -1)) and (currSearchFileExt == searchExt):
                #{
                    currFileNames.append(currSearchFileName)
                    dataLabels.append(utils_fx.Utils_RemoveFileNameExt(currSearchFileName))
                    dataNames.append(currSearchFileName)
                    flattenData.append(currFlattenData)
                    dataSkips.append(currSkipData)
                #}
            #}
        #}
        else:
        #{
            currFileNames.append(currFileDesc)
            dataLabels.append(utils_fx.Utils_RemoveFileNameExt(currFileDesc))
        #}
        
        for j in range(len(currFileNames)):
        #{
            rawData.append([])
            Data_LoadDataFromFile(dataDirectory + currFileNames[j], rawData[len(rawData) - 1])
        #}
    #}

    data = []
    idx = 0
    
    utils_fx.Utils_CheckEvenListSizes(rawData)

    while (True):
    #{
        datasLeft = len(rawData)

        for i in range(len(rawData)):
        #{
            currRawData = rawData[i]
            
            if (len(currRawData) > idx):
            #{
                data.append(currRawData[idx])
                data.append(currRawData[idx + 1])
            #}
            else:
            #{
                datasLeft -= 1
            #}
        #}

        if (datasLeft < 0):
            raise ValueError("Data tracker became negative while attempting to combine file data!")
        elif (datasLeft == 0):
            break

        idx += 2
    #}

    return data
#}

def Data_LoadDataFromFile(filePath, data):
#{
    main_fx.Main_CheckFile(filePath)

    file = open(filePath, "r+")

    main_fx.Main_StatusPrint("Gathering data from data file \"" + filePath + "\"...", 0)

    xData = []
    yData = []
    wordBuff = [""]
    numInserted = 0
    numDataLines = 0
    searchingHASP = False
    dataRatio = False
    lastTimeHASP = -1
    dataMult = 1
    #getcontext().prec = 6

    while (True):
    #{
        line = file.readline()
        canInsert = False

        if not (line):
        #{
            break
        #}
        elif (line == "\n"):
        #{
            continue
        #}
        elif (line.find("--") != -1):
        #{
            searchingHASP = True

            continue
        #}
        elif ((line.find("#") != -1) or (line.find("[") != -1)):
        #{
            dataRatio = True

            continue
        #}

        idx = 0

        for i in range(len(line)):
        #{
            currChar = line[i]

            if (currChar == ' '):
            #{
                continue
            #}
            elif (searchingHASP == False) and ((currChar == ',') or (currChar == ';')):
            #{
                wordBuff.append("")
                idx += 1
            #}
            else:
            #{
                wordBuff[idx] += currChar
            #}
        #}

        for i in range(len(wordBuff)):
        #{
            currWord = wordBuff[i]

            if (currWord.find(":") != -1):
            #{
                data.append(numDataLines)
            #}
            else:
            #{
                if (searchingHASP == True):
                #{
                    nums = currWord.split("\t")

                    for j in range(len(nums)):
                        if (nums[j].find("\n") != -1):
                            nums[j] = nums[j][0 : (len(nums[j]) - 1)]

                    temp = round(float(nums[len(nums) - 2]), 3)
                    time = round(float(nums[len(nums) - 1]), 3)

                    if (time != lastTimeHASP):
                    #{
                        data.append(time)
                        data.append(temp)

                        lastTimeHASP = time
                        numDataLines += 1
                    #}
                    else:
                    #{
                        data[len(data) - 1] = (data[len(data) - 1] + temp) / 2
                    #}
                #}
                else:
                #{
                    currNum = float(currWord)

                    if ((i % 2) != 0):
                        yData.append(10 * (np.log10(currNum)))
                    else:
                        xData.append(10000000 / currNum)

                    numDataLines += 1
                #}
            #}
        #}
    
        wordBuff = [""]
        numInserted += len(wordBuff)
    #}

    xData.reverse()
    yData.reverse()

    for i in range(len(xData)):
    #{
        data.append(xData[i])
        data.append(yData[i])
    #}

    file.close()

    if ((numInserted % 2) != 0):
        main_fx.Main_StatusPrint("The amount of data gathered from the data file is not even.", 4)

    main_fx.Main_StatusPrint("Successfully gathered data from data file.", 1)
#}