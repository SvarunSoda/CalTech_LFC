import os
import time
import sys
import clr
import numpy as np

clr.AddReference("C:\\Program Files\\Thorlabs\\ThorSpectra\\ThorlabsOSAWrapper.dll")

from System import Array
from System import Double
from ThorlabsOSAWrapper import *
from ThorlabsOSAWrapper import InstrumentModel
from ThorlabsOSAWrapper import AcquisitionUpdateFlag
from ThorlabsOSAWrapper import SpectrumStruct
from ThorlabsOSAWrapper import FileIOInterface

## CHANGEABLE ##
AverageNum = 5
SpectrumNum = 2
Sensitivity = 1
Resolution = 1
OutputDataSpacer = ';'
AcquisitionWait = 10

## DO NOT CHANGE ##
Data = []
LastHeader = []
SpectrumsCreated = 0
IterTracker = 0

def WriteSpectrumToFile(filePath, data):
    global OutputDataSpacer

    file = open(filePath, "w")
    
    for i in range(len(LastHeader)):
        file.write(LastHeader[i])

    idx = 0

    while (idx < len(data)):
        file.write(str(data[idx]) + OutputDataSpacer + str(data[idx + 1]) + "\n")

        idx += 2

    file.write("[EndOfFile]")

    file.close()

def LoadSpectrumFromFile(filePath):
    global LastHeader
    LastHeader = []

    file = open(filePath, "r+")

    data = []
    xData = []
    yData = []
    wordBuff = [""]
    numInserted = 0
    numDataLines = 0

    while (True):
        line = file.readline()

        if not (line):

            break

        elif (line == "\n"):

            continue

        elif ((line.find('#') != -1) or (line.find('[') != -1)):

            LastHeader.append(line)

            continue

        idx = 0

        for i in range(len(line)):
            currChar = line[i]

            if (currChar == ' '):

                continue

            elif ((currChar == ',') or (currChar == ';')):
                wordBuff.append("")
                idx += 1

            else:
                wordBuff[idx] += currChar

        for i in range(len(wordBuff)):
            currNum = float(wordBuff[i])

            if ((i % 2) != 0):
                #yData.append(10 * (np.log10(currNum)))
                yData.append(currNum)

            else:
                #xData.append(10000000 / currNum)
                xData.append(currNum)

            numDataLines += 1
    
        wordBuff = [""]
        numInserted += len(wordBuff)

    #xData.reverse()
    #yData.reverse()

    for i in range(len(xData)):
    #{
        data.append(xData[i])
        data.append(yData[i])
    #}

    file.close()

    return data

def OnContinuousAcquisitionUpdate(sender, event_args):
    global AverageNum

    global Data
    global SpectrumsCreated
    global IterTracker

    if (event_args.CallbackMessage.LastDataTypeUpdateFlag == AcquisitionUpdateFlag.Spectrum):
        file_interface = FileIOInterface()
        saveDir = os.getcwd()

        if (IterTracker == AverageNum):
            WriteSpectrumToFile(str(saveDir + r'\\spectrum_' + str(SpectrumsCreated + 1) +'.txt'), Data)

            print('Spectrum ' + str(SpectrumsCreated + 1) + ' saved!')

            SpectrumsCreated += 1
            IterTracker = 0

        else:
            spectrum = SpectrumStruct(sender.ChannelInterfaces[0].GetLastSpectrumLength(), True)
            sender.ChannelInterfaces[0].GetLastSpectrum(spectrum)

            fileName = '\\tempSpectrum_' + str(IterTracker) + '.txt'
            file_interface.WriteSpectrum(spectrum, saveDir + fileName, 1)

            spectrumData = LoadSpectrumFromFile(saveDir + fileName)
            os.remove(saveDir + fileName)

            if (IterTracker == 0):
                for i in range(len(spectrumData)):
                    Data.append(spectrumData[i])

            else:
                for i in range(len(spectrumData)):
                    if ((i % 2) == 0):
                        Data[i] = (Data[i] + spectrumData[i]) / 2

            print('Spectrum ' + str(SpectrumsCreated + 1) + ' averaged ' + str(IterTracker + 1) + ' time(s)!')

            IterTracker += 1

def main():
    print("---- SCRIPT STARTED ----\n")

    osa = 0
    locator = DeviceLocator()

    if (locator.InitializeSpectrometers() > 0): 
        print('Spectrometer found, opening...')

        osa = LibDeviceInterface(0)

    else:
        print('No devices found, starting simulator...')

        device_index = DeviceLocator.CreateVirtualSpectrometer(InstrumentModel.VirtualOSA203)
        peak_num = 2
        peak_amplitude_array = Array[Double]([.6, .3])
        fwhm_array = Array[Double]([20, 12])
        center_wavelength_array = Array[Double]([1200, 1865])

        virtual_config = VirtualSpectrometerConfiguration(peak_num)
        virtual_config.peakAmplitude = peak_amplitude_array
        virtual_config.fwhm_nm = fwhm_array
        virtual_config.centerWavelength_nm = center_wavelength_array

        DeviceLocator.ConfigureVirtualSpectrometer(device_index, virtual_config)

        time.sleep(1)

        osa = LibDeviceInterface(device_index)

    print('Device open!\n')

    global AverageNum
    global SpectrumNum
    global Sensitivity
    global Resolution
    global AcquisitionWait

    global Data
    global SpectrumsCreated
    global IterTracker

    osa.SetSensitivityMode(Sensitivity)
    osa.SetResolutionMode(Resolution)

    osa.OnContinuousAcquisitionUpdate += OnContinuousAcquisitionUpdate

    for i in range(SpectrumNum):
        print('Acquiring spectrum ' + str(SpectrumsCreated + 1) + '...')

        Data = []

        osa.StartContinuousAcquisition(AverageNum + 1)

        time.sleep(AcquisitionWait)

        IterTracker = 0

        if (i != (SpectrumNum - 1)):
            print(" ")

    osa.CloseSpectrometer

    print('\nDevice closed!')

    print("\n---- SCRIPT FINISHED ----")

if __name__ == "__main__":
    main()