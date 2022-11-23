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
Gen_ProgramName = "CalTech - LFC Flatter Simulation Program"
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

Prog1_GaussianSigma = None                          #1
Prog1_GaussianPhis = []                             #22
Prog1_GraphViewport = [
    [None, None],                                   #3, 4
    [None, None]                                    #5, 6
    ]
Prog1_GraphAccuracy = None                          #7

#### MAIN PROGRAM FUNCTIONS ####
def main():
#{
    Main_DeleteFile(os.getcwd().replace("\\", Main_GetPathSeparator()) + Main_GetPathSeparator() + Gen_CursorPosFileName)

    Main_InitProgram()
    Main_VersionPrints()

    Main_ProgramFlattenerSim()

    Main_StatusPrint("---- PROGRAM EXITED ----", 2)
#}

def Main_ProgramFlattenerSim(): #1
#{
    gaussianSigmas = []
    gaussianPhis = []
    gaussianAmplitudes = []
    dataLabels = []

    for i in range(len(Prog1_GaussianPhis)):
    #{
        currPhi = Prog1_GaussianPhis[i]

        gaussianSigmas.append(Prog1_GaussianSigma)
        gaussianPhis.append(currPhi)
        gaussianAmplitudes.append(1)
        dataLabels.append("Gaussian #" + str(i) + " (phi: " + str(currPhi) + ")")
    #}

    dataLabels.append("Gaussian Sum")

    data = math_fx.Math_GenerateGaussianData(gaussianSigmas, 
                                            gaussianPhis,
                                            Prog1_GraphViewport[0][0], 
                                            Prog1_GraphViewport[0][1], 
                                            Prog1_GraphAccuracy,
                                            gaussianAmplitudes,
                                            1410,
                                            [],
                                            [],
                                            [],
                                            True,
                                            True)
    xData = []
    yData = []

    data_fx.Data_SeparateXYData(data, xData, yData)

    graphing_fx.Graphing_GraphDataPoints(xData, yData, 
                                        Prog1_GraphViewport[0], 
                                        Prog1_GraphViewport[1], 
                                        dataLabels,
                                        [],
                                        [Gen_ProgramName + " v" + str(Gen_ProgramVersion) + " (Sigma: " + str(Prog1_GaussianSigma) + ", Peak #: " + str(len(Prog1_GaussianPhis)) + ")", "Spectrum (nm)", "Level (db)"],
                                        Gen_GraphConfig, 
                                        False,
                                        None, 
                                        [False, False],
                                        True, "", "")
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

        global Prog1_GaussianSigma
        global Prog1_GaussianPhis
        global Prog1_GraphViewport
        global Prog1_GraphAccuracy

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

    global Prog1_GaussianSigma          #1
    global Prog1_GaussianPhis           #22
    global Prog1_GraphViewport          #3 - 6
    global Prog1_GraphAccuracy          #7

    math_fx = None
    graphing_fx = None

    Gen_WorkingDirectory = None
    Gen_GraphConfig = [None, None, None, None, None, None, None, None, None, None, None]

    Prog1_GaussianSigma = None
    Prog1_GaussianPhis = []
    Prog1_GraphViewport = [[None, None], [None, None]]
    Prog1_GraphAccuracy = None
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