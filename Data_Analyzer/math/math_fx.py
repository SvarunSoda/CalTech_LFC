#### MATH FUNCTION DEFINITIONS ####

#### BASE IMPORTS ####
import math
import numpy as np
from scipy import optimize
import matplotlib.pyplot as plt

#### MY IMPORTS ####
import main_fx
import utils_fx

def Math_FitSineToData(xData, yData):
#{
    plt.figure(figsize=(14, 8))

    newXData = []
    newYData = []
    idxLimit = 0
    localIdx = 0

    for i in range(len(xData)):
    #{
        if (localIdx == idxLimit):
        #{
            newXData.append(xData[i])
            newYData.append(yData[i])

            localIdx = 0

            continue
        #}

        localIdx += 1
    #}

    maxNewY = max(newYData)
    minNewY = min(newYData)

    guessValues = [
        ((maxNewY - minNewY) / 2),
        0.05,
        newXData[utils_fx.Utils_FindInList(newYData, maxNewY)],
        Math_ListAverage([maxNewY, minNewY])
        ]

    sineParams, sineParamsCovariance = optimize.curve_fit(Math_GetSineValueY, newXData, newYData, p0 = guessValues, maxfev = 100000000)

    sineDataX = []
    sineDataY = []

    for i in range(len(xData)):
    #{
        sineDataX.append(xData[i])
        sineDataY.append(Math_GetSineValueY(xData[i], sineParams[0], sineParams[1], sineParams[2], sineParams[3]))
        #sineDataY.append(Math_GetSineValueY(xData[i], guessValues[0], guessValues[1], guessValues[2], guessValues[3]))
    #}

    plt.scatter(newXData, newYData, label = 'Data')
    plt.plot(sineDataX, sineDataY, label = 'Fitted function')
    
    plt.legend(loc='best')
    
    plt.show()
    
    plt.close()

    return sineParams
#}

def Math_GetSineValueY(x, amplitude, stretch, horzShift, vertShift):
#{
    return (amplitude * (np.sin((x * stretch) + horzShift) + vertShift))
#}

#TODO: Separate sum function
def Math_GenerateGaussianData(sigmas, phis, xStart, xEnd, iterations, amplitudes, xAxisStart, xPoints, yFitPoints, muList, calculateSum, logAnswer):
#{
    main_fx.Main_StatusPrint("Attempting to generate Gaussian data...", 0)

    if (xEnd <= xStart):
        raise ValueError("Attempting to acquire Gaussian data, but the ending X value is equal to or smaller than the starting X value!")
    if (len(sigmas) == 0):
        raise ValueError("Attempting to acquire Gaussian data, but the number of desired peaks is 0!")
    if (len(amplitudes) == 0):
        raise ValueError("Attempting to acquire Gaussian data, but the number of desired amplitudes is 0!")
    if (len(sigmas) != len(amplitudes)):
        raise ValueError("Attempting to acquire Gaussian data, but the amount of datas isn't equal!")
    if (len(phis) != len(amplitudes)):
        raise ValueError("Attempting to acquire Gaussian data, but the amount of datas isn't equal!")
    if (((len(xPoints) == 0) and not (iterations > 0)) or ((len(xPoints) > 0) and not (iterations <= 0))):
        raise ValueError("Attempting to acquire Gaussian data, but the number of desired iterations is 0 or less!")
    if ((len(xPoints) > 0) and (len(xPoints) != len(yFitPoints))):
        raise ValueError("Attempting to acquire Gaussian data, but the sizes of provided X and Y data points aren't equal!")

    mus = [0]
    peaks = len(sigmas)

    for i in range(peaks - 1):
    #{
        currSigma = sigmas[i + 1]
        currPhi = phis[i + 1]
        currAmplitude = amplitudes[i + 1]

        halfY = (Math_GetGaussianValueY(0, 0, currSigma, currPhi, currAmplitude, logAnswer) / 2)
        halfX = Math_GetGaussianValueX(halfY, 0, currSigma, currPhi, currAmplitude, logAnswer)[0]

        mus.append((halfX * 2) + mus[i])
    #}

    muOffset = (xAxisStart - mus[0])

    if (logAnswer == True):
        for i in range(len(sigmas)):
            sigmas[i] *= 0.31675

    for i in range(len(mus)):
    #{
        mus[i] += muOffset
        muList.append(mus[i])
    #}

    if (len(yFitPoints) > 0):
        for i in range(len(amplitudes)):
            amplitudes[i] = yFitPoints[utils_fx.Utils_FindInList(xPoints, Math_GetClosestNum(mus[i], xPoints))]

    main_fx.Main_LoadingStart("Generating Gaussian Data...")

    data = []
    xCurr = xStart
    xInc = None
    loopRuns = iterations
    #yInc = None

    if (len(xPoints) == 0):
        xInc = ((xEnd - xStart) / iterations)
    else:
        loopRuns = len(xPoints)

    for i in range(loopRuns):
    #{
        if (xInc == None):
            xCurr = xPoints[i]
        else:
            xCurr += xInc
        
        yCurrSum = 0

        for j in range(peaks):
        #{
            yCurr = Math_GetGaussianValueY(xCurr, mus[j], sigmas[j], phis[j], 1, logAnswer)

            #xCurr = Math_GetGaussianValueX(-3, mus[j], sigmas[j], phis[j], 1, logAnswer)
            #spacing = xCurr[0] - xCurr[1]

            #if (logAnswer == True):
            ##{
            #    if (yCurr < 0.0001):
            #    #{
            #        yCurr = 0
            #    #}
            #    else:
            #    #{
            #        if (yInc == None):
            #            yInc = yCurr
            #        
            #        yCurr += -(yInc)
            #    #}
            ##}

            #if (amplitudes[j] < -6) and (yCurr > 0.9):
            #    bruh = 0

            yCurr *= amplitudes[j]

            data.append(xCurr)
            data.append(yCurr)

            yCurrSum += yCurr
        #}

        if (calculateSum == True):
        #{
            data.append(xCurr)
            data.append(yCurrSum)
        #}

        main_fx.Main_LoadingProgress((i + 1), loopRuns, "Generating Gaussian Data...")
    #}

    main_fx.Main_LoadingEnd()
    main_fx.Main_StatusPrint("Successfully generated Gaussian data.", 1)

    return data
#}

def Math_GetGaussianValueX(y, mu, sigma, phi, amplitude, usingLog):
#{
    x = None

    if ((usingLog == True) and (y > 0)):
        y = np.log10(y)

    if (usingLog == True):
        x = ((sigma * np.sqrt(-2 * np.log(np.power(float(10), y) / (amplitude * np.cos(phi))))) + mu)
    else:
        x = ((sigma * np.sqrt(-2 * np.log(y / (amplitude * np.cos(phi))))) + mu)

    if ((math.isnan(x) == True) or (math.isinf(x) == True)):
        raise ValueError("X value(s) of Gaussian is nan or inf!")

    return [x, (mu - (x - mu))]
#}

def Math_GetGaussianValueY(x, mu, sigma, phi, amplitude, usingLog):
#{
    y = ((amplitude * np.cos(phi)) * np.exp(-np.power(((x - mu) / sigma), 2) / 2))

    if (usingLog == True):
        if (y < 0.1):
            return 0
        else:
            y = np.log10(y) + 1

    if ((math.isnan(y) == True) or (math.isinf(y) == True)):
        raise ValueError("Y value of Gaussian is nan or inf!")

    return y
#}

def Math_InterpolatePointsLinear(points):
#{
    if ((len(points) % 2) != 0):
        raise ValueError("Attempting to interpolate linearly some points, but the amount of points isn't even!")
    if (len(points) < 4):
        raise ValueError("Attempting to interpolate linearly some points, there aren't enough points (at least 2)!")

    pointNum = (len(points) / 2)
    sumX = 0
    sumY = 0

    for i in range(len(points)):
        if ((i % 2) == 0):
            sumX += points[i]
        else:
            sumY += points[i]

    meanX = (sumX / pointNum)
    meanY = (sumY / pointNum)
    slopeDividend = 0
    slopeDivisor = 0

    for i in range(len(points)):
    #{
        if ((i % 2) == 0):
        #{
            slopeDividend += ((points[i] - meanX) * (points[i + 1] - meanY))
            slopeDivisor += ((points[i] - meanX) * (points[i] - meanX))
        #}
    #}

    slope = 0

    if (slopeDivisor == 0):
        raise ValueError("Attempting to interpolate linearly some points, but the slope divisor is 0!")
    else:
        slope = (slopeDividend / slopeDivisor)

    yIntercept = (meanY - (slope * meanX))

    return [yIntercept, slope]
#}

def Math_GetPolynomialValueY(x, function):
#{
    if (len(function) == 0):
        raise ValueError("Attempting to get the value of a polynomial function, but the function is empty!")

    y = function[0]
    idx = 1

    while (idx < len(function)):
    #{
        y += (function[idx] * np.power(x, idx))
        
        idx += 1
    #}

    return y
#}

def Math_GetClosestNum(base, nums):
#{
    if (len(nums) == 0):
        raise ValueError("Attempting to get closest number of no numbers!")

    closestIdx = 0
    closestDiff = np.abs(base - nums[0])
    idx = 1

    while (idx < len(nums)):
    #{
        currDiff = np.abs(base - nums[idx])

        if (currDiff < closestDiff):
        #{
            closestDiff = currDiff
            closestIdx = idx
        #}

        idx += 1
    #}

    return nums[closestIdx]
#}

def Math_ListAverage(lst):
#{
    return (sum(lst) / len(lst))
#}