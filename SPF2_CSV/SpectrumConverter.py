import os
import time
import sys
import clr

clr.AddReference("C:\\Program Files\\Thorlabs\\ThorSpectra\\ThorlabsOSAWrapper.dll")

SpectrumInputs = [
    "C:\\Users\\SVARUN\\Desktop\\work\\caltech\\scripting\\TEST\\Spectrum_1.spf2",
    "C:\\Users\\SVARUN\\Desktop\\work\\caltech\\scripting\\TEST\\Spectrum_2.spf2"
    ]
SpectrumOutputFormat = 1

from ThorlabsOSAWrapper import *
from ThorlabsOSAWrapper import SpectrumStruct
from ThorlabsOSAWrapper import FileIOInterface

SpectrumOutputs = [
    ".spf2",    #0
    ".txt"      #1
    ]

def main():

    print("Converting the following SPF2 spectrum files to TXT:")

    for i in range(len(SpectrumInputs)):
        print("\t- \"" + SpectrumInputs[i] + "\"")

    print(" ")

    fileInterface = FileIOInterface()

    for i in range(len(SpectrumInputs)):
        traceNum = fileInterface.CountSpectraInFile(SpectrumInputs[i])

        print(str(traceNum) + " trace(s) found in \"" + SpectrumInputs[i] + "\".")

        for j in range(traceNum):
            spectrum = SpectrumStruct(1)
            fileInterface.ReadSpectrum(spectrum, SpectrumInputs[i], j)

            fileInterface.WriteSpectrum(spectrum, SpectrumInputs[i][0 : len(SpectrumInputs[i]) - 5] + "_" + str(j + 1) + SpectrumOutputs[SpectrumOutputFormat], SpectrumOutputFormat)

    print("\n-- FINISHED --")

if __name__ == "__main__":
    main()