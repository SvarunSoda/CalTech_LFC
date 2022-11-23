#### FLATTENING FUNCTION DEFINITIONS ####

#### BASE IMPORTS ####
import numpy as np

#### MY IMPORTS ####
import main_fx
import math_fx
import data_fx
import utils_fx

def Math_FlattenDatas(xData, yData, flattenLimits, flattenIndices):
#{
    data_fx.Data_CheckSeparatedXYData(xData, yData)

    if (len(xData) != len(flattenIndices)):
        raise ValueError("The amount of data and the amount of flattening indices are not equal!")
    if (len(flattenLimits) != 2):
        raise ValueError("The flatten limits aren't 2!")

    for i in range(len(flattenIndices)):
    #}
        if (len(flattenIndices[i]) == 0):
            raise ValueError("There is no current flattening data!")

        currFlattenData = flattenIndices[i]
        currFlattenIdx = currFlattenData[0]

        if (currFlattenIdx == -1):
            continue

        main_fx.Main_StatusPrint("Attempting to flatten some data points...", 0)

        flattenArgumentNum = len(flattenIndices[i])
        startIdx = utils_fx.Utils_FindInList(xData[i], math_fx.Math_GetClosestNum(flattenLimits[0], xData[i]))
        endIdx = utils_fx.Utils_FindInList(xData[i], math_fx.Math_GetClosestNum(flattenLimits[1], xData[i]))

        if ((startIdx == -1) or (endIdx == -1)):
            raise ValueError("Starting or ending indices failed to be found!")
        if (startIdx > endIdx):
            raise ValueError("Starting index is higher than ending index!")

        chosenXData = []
        chosenYData = []
        idx = startIdx

        while (idx < endIdx):
        #{
            chosenXData.append(xData[i][idx])
            chosenYData.append(yData[i][idx])

            idx += 1
        #}

        if (currFlattenIdx == 0):
        #{
            if (flattenArgumentNum != 3):
                raise ValueError("Slope-flattening was requested, but amount of flattening arguments is not 3!")

            chosenYData = Math_GetSlopeFlattenedData(chosenXData, chosenYData, currFlattenData[1], currFlattenData[2])
        #}
        elif (currFlattenIdx == 1):
        #{
            if (flattenArgumentNum != 2):
                raise ValueError("Point-flattening was requested, but amount of flattening arguments is not 2!")

            chosenYData = Math_GetPointFlattenedData(chosenXData, chosenYData, currFlattenData[1])
        #}
        elif (currFlattenIdx == 2):
        #{
            if (flattenArgumentNum != 6):
                raise ValueError("Gaussian-flattening was requested, but amount of flattening arguments is not 6!")

            chosenYData = Math_GetGaussianFlattenedData(chosenXData, chosenYData, currFlattenData[1], currFlattenData[2], currFlattenData[3], currFlattenData[4], currFlattenData[5])
        #}
        else:
        #{
            raise ValueError("This type of flattening has not been implemented yet!")
        #}

        idx = 0

        while (idx < (endIdx - startIdx)):
        #{
            yData[i][idx + startIdx] = chosenYData[idx]

            idx += 1
        #}

        main_fx.Main_StatusPrint("Successfully flattened some data points.", 1)
    #}

    data_fx.Data_CheckSeparatedXYData(xData, yData)
#}

def Math_GetGaussianFlattenedData(xData, yData, reachPercentage, flattenNum, sigma, phi, amplitude):
#{
    flattenedYData = yData

    for i in range(int(flattenNum)):
    #{
        flattenedYData = Math_GaussianFlattenData(xData, flattenedYData, reachPercentage, sigma, phi, amplitude)

        main_fx.Main_StatusPrint("Data was Gaussian-flattened " + str(i + 1) + " times.", 0)
    #}

    return flattenedYData
#}

def Math_GaussianFlattenData(xData, yData, reachPercentage, sigma, phi, amplitude):
#{
    Math_CheckDataForFlattening(xData, yData)

    if (reachPercentage <= 0.001):
        raise ValueError("Attempting to get Gaussian-flattened data, but the reach percentage is too small or negative!")

    main_fx.Main_LoadingStart("Gaussian-Flattening Data...")

    flattenedYData = []
    localPointNum = 1
    xStep = 0

    for i in range(len(xData)):
    #{
        gaussianCenter = xData[i]
        originalY = yData[i]
        baseReachEdges = math_fx.Math_GetGaussianValueX((math_fx.Math_GetGaussianValueY(0, 0, sigma, phi, amplitude, False) * reachPercentage), 0, sigma, phi, amplitude, False)
        reachEdges = [(gaussianCenter + baseReachEdges[0]), (gaussianCenter + baseReachEdges[1])]
        
        currYPoints = [yData[i]]
        kernel = [math_fx.Math_GetGaussianValueY(gaussianCenter, gaussianCenter, sigma, phi, amplitude, True)]

        for j in range(2):
        #{
            idx = i
            centerIdx = i
            currReachEdge = reachEdges[j]
            inc = 1
            xPrev = gaussianCenter

            if (j == 1):
                inc = -1

            idx += inc

            while (True):
            #{
                currXPoint = None
                insYValue = 0

                if ((idx >= 0) and (idx < len(yData))):
                #{
                    currXPoint = xData[idx]
                    insYValue = yData[idx]
                #}
                else:
                #{
                    bruh = 0

                    break
                #}

                if ((i == 0) and (j == 0)):
                #{
                    if (currXPoint > currReachEdge):
                    #{
                        break
                    #}
                    else:
                    #{
                        localPointNum += 1

                        newXStep = round((currXPoint - xPrev), 2)

                        if ((idx > 1) and (xStep != newXStep)):
                            raise ValueError("X step value has changed!")

                        xStep = newXStep
                        xPrev = currXPoint
                    #}
                #}
                else:
                #{
                    if ((idx >= (centerIdx + localPointNum)) or (idx <= (centerIdx - localPointNum))):
                    #{
                        break
                    #}
                #}

                if (j == 0):
                #{
                    currYPoints.append(insYValue)
                    kernel.append(math_fx.Math_GetGaussianValueY(((idx - centerIdx) * xStep), 0, sigma, phi, amplitude, False))
                #}
                else:
                #{
                    currYPoints.insert(0, insYValue)
                    kernel.insert(0, math_fx.Math_GetGaussianValueY(((idx - centerIdx) * xStep), 0, sigma, phi, amplitude, False))
                #}

                idx += inc
            #}
        #}

        if (len(kernel) != len(currYPoints)):
            raise ValueError("Attempting to get Gaussian-flattened data, but the sizes of the kernel and data buffer got disconnected!")

        kernelSum = sum(kernel)

        for j in range(len(kernel)):
            kernel[j] = (kernel[j] / kernelSum)

        newCurrYPoints = []

        for j in range(len(currYPoints)):
            newCurrYPoints.append(currYPoints[j] * kernel[j])

        flattenedYData.append(sum(newCurrYPoints))

        main_fx.Main_LoadingProgress((i + 1), len(xData), "Gaussian-Flattening Data...")
    #}

    main_fx.Main_LoadingEnd()

    return flattenedYData
#}

def Math_GetSlopeFlattenedData(xData, yData, flattenPercent, flattenNum):
#{
    flattenedYData = yData

    if (flattenNum > 1):
        main_fx.Main_LoadingStart("Slope-Flattening Data...")

    for i in range(int(flattenNum)):
    #{
        flattenedYData = Math_SlopeFlattenData(xData, flattenedYData, flattenPercent, ((i % 2) == 0))

        #main_fx.Main_StatusPrint("Data was slope-flattened " + str(i + 1) + " times.", 0)
        if (flattenNum > 1):
            main_fx.Main_LoadingProgress((i + 1), flattenNum, "Slope-Flattening Data...")
    #}

    if (flattenNum > 1):
        main_fx.Main_LoadingEnd()

    return flattenedYData
#}

def Math_SlopeFlattenData(xData, yData, flattenPercent, shiftFront):
#{
    Math_CheckDataForFlattening(xData, yData)

    if (flattenPercent == 0):
        raise ValueError("Attempting to get slope-flattened data, but the flattening percentage is 0!")

    flattenedYData = []
    flattenedYData.append(yData[0])
    idx = 1

    while (idx < len(xData)):
    #{
        points = []
        main_fx.Main_ResizeList(points, 4)

        points[0] = 0
        points[1] = yData[idx - 1]
        points[2] = 1
        points[3] = yData[idx]

        if (shiftFront == True) and (idx != (len(xData) - 1)):
        #{
            points[1] = yData[idx]
            points[3] = yData[idx + 1]
        #}

        equation = math_fx.Math_InterpolatePointsLinear(points)
        equation[1] *= flattenPercent

        newYData = math_fx.Math_GetPolynomialValueY(1, equation)

        flattenedYData.append(newYData)

        idx += 1
    #}

    return flattenedYData
#}

def Math_GetPointFlattenedData(xData, yData, pointNum):
#{
    flattenedYData = Math_PointFlattenData(xData, yData, int(pointNum))

    main_fx.Main_StatusPrint("Data was point-flattened.", 0)

    return flattenedYData
#}

def Math_PointFlattenData(xData, yData, pointNum):
#{
    Math_CheckDataForFlattening(xData, yData)

    if (pointNum == 0):
        raise ValueError("Attempting to get point-flattened data, but the point number is 0!")

    flattenedYData = []
    idx = 0

    while (idx < len(xData)):
    #{
        points = []
        currPointNum = 0

        while (currPointNum < pointNum) and ((idx + currPointNum) < len(xData)):
            currPointNum += 1

        for i in range(currPointNum):
        #{
            points.append(xData[idx + i])
            points.append(yData[idx + i])
        #}

        equation = math_fx.Math_InterpolatePointsLinear(points)

        for i in range(currPointNum):
            flattenedYData.append(math_fx.Math_GetPolynomialValueY(xData[idx + i], equation))

        idx += currPointNum
    #}

    return flattenedYData
#}

def Math_CheckDataForFlattening(xData, yData):
#{
    if (len(xData) != len(yData)):
        raise ValueError("Attempting to get flattened data, but the amount of X and Y datas are not equal!")
    if (len(xData) == 0):
        raise ValueError("Attempting to get flattened data, but there is no X data present!")
    if (len(xData) == 1):
        raise ValueError("Attempting to get flattened data, but there is only one X data point present!")
    if (len(yData) == 0):
        raise ValueError("Attempting to get flattened data, but there is no Y data present!")
    if (len(yData) == 1):
        raise ValueError("Attempting to get flattened data, but there is only one Y data point present!")
#}