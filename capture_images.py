import io
import time
import numpy as np
import cv2
from ctypes import *
import os.path
import sys
import os
import datetime

os.environ['path'] += ';.\\camera'
libKsj = WinDLL("KSJApi64.dll")
libKsj.KSJ_Init()
camCount = libKsj.KSJ_DeviceGetCount()


g_gain = 250
g_gamma = 0
g_contrast = 30
g_brigthness = 0
g_exposurelines = 3000
libKsj.KSJ_SetParam(0, 1, g_gain)
libKsj.KSJ_SetParam(0, 2, g_gain)
libKsj.KSJ_SetParam(0, 3, g_gain)
libKsj.KSJ_SetParam(0, 4, g_gamma)
libKsj.KSJ_SetParam(0, 14, g_contrast)
libKsj.KSJ_SetParam(0, 15, g_brigthness)
libKsj.KSJ_SetParam(0, 23, g_exposurelines)

while True:
    usDeviceType = c_int()
    nSerials = c_int()          
    usFirmwareVersion = c_int()
    libKsj.KSJ_DeviceGetInformation(0, byref(usDeviceType), byref(nSerials), byref(usFirmwareVersion))
    nWidth = c_int()
    nHeight = c_int()
    nBitCount = c_int()
    libKsj.KSJ_CaptureGetSizeEx(0, byref(nWidth), byref(nHeight), byref(nBitCount))
    trigermode = c_int()
    libKsj.KSJ_TriggerModeGet(0, byref(trigermode))
    nbufferSize = nWidth.value * nHeight.value * nBitCount.value / 8
    pRawData = create_string_buffer(int(nbufferSize))
    retValue = libKsj.KSJ_CaptureRgbData(0, pRawData)
    image = np.frombuffer(pRawData, np.uint8).reshape(nHeight.value, nWidth.value, int(nBitCount.value/8))

#####################################################################################################

    today = datetime.datetime.now()
    t = time.strftime("%I-%M-%S%p")
    file_name = today.strftime('%d-%m-%Y') + '__' + t
    date_time=today.strftime('%Y/%m/%d %I:%M:%S')
    cv2.imwrite("output_images2/{}.jpg".format(file_name),image)
    libKsj.KSJ_EmptyFrameBuffer(0)