#### UTILS FUNCTION DEFINITIONS ####

#### MY IMPORTS ####
import main_fx

def Utils_GenerateOccurenceList(lists):
#{
    occurenceList = [sorted(Utils_UnionLists(lists)), []]

    for i in range(len(occurenceList[0])):
        occurenceList[1].append(0)

    for i in range(len(lists)):
    #{
        currList = lists[i]

        for j in range(len(currList)):
        #{
            currWord = currList[j]

            occurenceList[1][Utils_FindInList(occurenceList[0], currWord)] += 1
        #}
    #}

    return occurenceList
#}

def Utils_MaxSizeOfLists(lists):
#{
    if (len(lists) == 0):
        raise ValueError("Attempting to get max size of no lists!")

    maxSize = len(lists[0])
    idx = 1

    while (idx < len(lists)):
    #{
        currSize = len(lists[idx])

        if (currSize > maxSize):
            maxSize = currSize

        idx += 1
    #}

    return maxSize
#}

def Utils_MinSizeOfLists(lists):
#{
    if (len(lists) == 0):
        raise ValueError("Attempting to get min size of no lists!")

    minSize = len(lists[0])
    idx = 1

    while (idx < len(lists)):
    #{
        currSize = len(lists[idx])

        if (currSize < minSize):
            minSize = currSize

        idx += 1
    #}

    return minSize
#}

def Utils_IntersectLists(lists, tolerance, doSort):
#{
    #if (len(lists) == 0):
    #    raise ValueError("Attempting to get intersection of no lists!")

    #intersection = []
    intersection = Utils_UnionLists(lists)

    if (doSort == True):
        intersection = sorted(intersection)

    nonIntersections = 0

    #for i in range(len(lists[0])):
    #    intersection.append(lists[0][i])

    i = 0

    while (i < len(lists)):
    #{
        currList = lists[i]
        j = 0
        deleteing = False

        while(j < len(intersection)):
        #{
            currSearchValue = intersection[j]
            searchValueIdx = Utils_FindInList(currList, currSearchValue)

            if (searchValueIdx == -1):
            #{
                if (nonIntersections >= tolerance):
                #{
                    del intersection[Utils_FindInList(intersection, currSearchValue)]

                    j =- 1
                #}
                else:
                #{
                    deleteing = True
                #}
            #}

            j += 1
        #}

        if (deleteing == True):
            nonIntersections += 1

        i += 1
    #}

    return intersection
#}

def Utils_UnionLists(lists):
#{
    if (len(lists) == 0):
        raise ValueError("Attempting to get union of no lists!")

    union = []

    for i in range(len(lists)):
    #{
        currList = lists[i]

        for j in range(len(currList)):
        #{
            currSearchValue = currList[j]

            if (Utils_FindInList(union, currSearchValue) == -1):
                union.append(currSearchValue)
        #}
    #}

    return union
#}

def Utils_FindInList(list, value):
#{
    for i in range(len(list)):
        if (list[i] == value):
            return i

    return -1
#}

def Utils_RemoveFileNameExt(fileName):
#{
    extPos = fileName.find(".")

    if (extPos != -1):
        return fileName[0 : extPos]
    
    return fileName
#}

def Utils_IsolateFileName(filePath):
#{
    if (len(filePath) == 0):
        return ""

    return filePath[(Utils_FindFileNameInPath(filePath) + 1) : len(filePath)]
#}

def Utils_IsolateFilePath(filePath):
#{
    if (len(filePath) == 0):
        return ""

    return filePath[0 : Utils_FindFileNameInPath(filePath)] + main_fx.Main_GetPathSeparator()
#}

def Utils_FindFileNameInPath(filePath):
#{
    if (len(filePath) == 0):
        return ""

    idx = len(filePath) - 1

    while (idx >= 0):
    #{
        currChar = filePath[idx]

        if (currChar == main_fx.Main_GetPathSeparator()):
            break

        idx -= 1
    #}

    return idx
#}

def Utils_GetLongestOfStrings(strings):
#{
    if (len(strings) == 0):
        raise ValueError("Attempting to get the longest string out of no strings!")
    
    longest = len(strings[0])

    for i in range(len(strings) - 1):
        if (len(strings[i + 1]) > longest):
            longest = len(strings[i + 1])

    return longest
#}

def Utils_GetShortestOfStrings(strings):
#{
    if (len(strings) == 0):
        raise ValueError("Attempting to get the shortest string out of no strings!")
    
    shortest = len(strings[0])

    for i in range(len(strings) - 1):
        if (len(strings[i + 1]) < shortest):
            shortest = len(strings[i + 1])

    return shortest
#}

def Utils_CheckEvenListSizes(lists):
#{
    if (len(lists) == 0):
        raise ValueError("Attempting to check eveness of the sizes of 0 lists!")

    for i in range(len(lists)):
        if ((len(lists[i]) % 2) != 0):
            raise ValueError("A list is not even!")
#}

def Utils_CheckEqualListSizes(lists):
#{
    if (len(lists) == 0):
        raise ValueError("Attempting to check equalness of the sizes of 0 lists!")

    size = len(lists[0])

    for i in range(len(lists) - 1):
        if (size != len(lists[i + 1])):
            raise ValueError("Lists are not equal!")
#}

def Utils_MaxOfLists(lists):
#{
    if (len(lists) == 0):
        raise ValueError("Attempting to get a maximum out of no lists!")

    allMax = max(lists[0])

    for i in range(len(lists) - 1):
    #{
        listMax = max(lists[i + 1])

        if (listMax > allMax):
            allMax = listMax
    #}

    return allMax
#}

def Utils_MinOfLists(lists):
#{
    if (len(lists) == 0):
        raise ValueError("Attempting to get a minimum out of no lists!")

    allMin = min(lists[0])

    for i in range(len(lists) - 1):
    #{
        listMin = min(lists[i + 1])

        if (listMin < allMin):
            allMin = listMin
    #}

    return allMin
#}