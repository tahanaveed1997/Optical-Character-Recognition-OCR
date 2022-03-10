import tkinter as tk
from tkinter.font import BOLD
from ttkthemes import ThemedTk
from tkinter.ttk import Button, Frame, Label, Style
import PIL.Image, PIL.ImageTk
import serial
import argparse
import sys
from pathlib import Path
import cv2
import numpy as np
import torch
import torch.backends.cudnn as cudnn
from numpy import random
from paddleocr import PaddleOCR, draw_ocr #OCR 
from scipy import ndimage #Image Rotation
import re #Regular Expression
import cv2
import numpy as np
import time
from models.experimental import attempt_load
from utils.augmentations import Albumentations, augment_hsv, copy_paste, letterbox
from utils.datasets import LoadStreams, LoadImages
from utils.general import check_img_size, check_imshow, check_requirements, check_suffix, colorstr, is_ascii, \
    non_max_suppression, apply_classifier, scale_coords, xyxy2xywh, strip_optimizer, set_logging, increment_path
    # save_one_box
from utils.plots import Annotator, colors
# from utils.torch_utils import select_device, load_classifier, time_sync
from utils.torch_utils import select_device, time_sync
import threading
from detect_text import detect
# from easyocr import Reader
from ctypes import *
import os.path
import sys
import os
import datetime
import keyboard
import pyodbc
import pandas as pd
from OCR._OCR_ import _OCR_


##################  CONNECT TO MSSQL DATABASE   ##########################################################################################


conn = pyodbc.connect('Driver={SQL Server};'
                    'Server=200.100.31.40;'
                    'username=sa;'
                    'password=asif12345;'
                    'Database=BoxOcrProject;'
                    'Trusted_Connection=yes;'
                      )

cursor = conn.cursor()

######################################################################################################################################################


############################ TAKING INPUT FROM CUSTOMER FOR USER_ID AND CONVEYOR_ID #############################################################

User_ID=input('PLEASE ENTER YOUR USER_ID TO CONTINUE: ')
Conveyor_ID=input('PLEASE ENTER YOUR CONVEYOR_ID: ')


# User_ID=0
ocr_data=""
Status="No Box"
# Conveyor_ID=" No Batch"

#############################################################################################################################################################################


ard=serial.Serial(port='COM9',baudrate=9600)

os.environ['path'] += ';.\\camera'
libKsj = WinDLL("KSJApi64.dll")
libKsj.KSJ_Init()
nWidth = c_int()
nHeight = c_int()
nBitCount = c_int()
libKsj.KSJ_CaptureGetSizeEx(0, byref(nWidth), byref(nHeight), byref(nBitCount))

g_nWidth = 3096
g_nHeight = 2080
g_nStartx = 0
g_nStarty = 0
g_skipmode = 0
# g_gain = 150
# g_exposure = 200
# g_gamma = 2
# g_contrast = 20
# g_brigthness = 30
# g_exposurelines = 2500
g_gain = 250
g_gamma = 0
g_contrast = 20
g_brigthness = 0
g_exposurelines = 2500


######################################################################################################################

class App:
    def __init__(self, window, window_title, height , width ):
        self.window = window
        self.window.title(window_title)
        self.height = height
        self.width = width
        self.counter=0
        set_logging()
        self.device = select_device('')
        self.half = self.device.type != 'cpu'  # half precision only supported on CUDA
        self.class_ocr = _OCR_()
        
        # Create a canvas that can fit the above video source size
        self.canvas = tk.Canvas(window, width = 800, height = 400)
        self.canvas.pack()
              
        style = Style()
        style.theme_use('breeze')
        style.configure("TButton", foreground="red",
                        background="light sky blue",  font=('Helvetica', 22))

        self.head_frame = Frame(self.canvas)
        self.head_frame.grid(row=0, column=0, columnspan=3, sticky="", pady=self.height*0.009)
        self.main_head = Label(self.head_frame, font=("Courier", 35 , BOLD), padding=0)
        self.main_head.grid(row=0, column=0, sticky="")
        self.main_head['text']="BOX OCR SYSTEM"

        self.frame1 = Frame(self.canvas)
        self.frame2 = Frame(self.canvas)
        self.frame3 = Frame(self.canvas)
        # self.frame1.grid(row=1, column=4, columnspan=1, sticky="w", pady=self.height*0.009 ,padx=self.width*0.09  )
        self.frame2.grid(row=2, column=1, columnspan=1, sticky="e", pady=self.height*0.009 )
        self.frame3.grid(row=3, column=1, columnspan=1, sticky="e", pady=self.height*0.009 )

        # video frame 
        # Create a canvas that can fit the above video source size
        self.canvas = tk.Canvas(self.frame2, width = 700, height = 500)
        self.canvas.grid(row=2, column=1, columnspan=1, sticky="", pady=self.height*0.009 ,  padx =self.width*0.009 )
        
    
        self.tf_label2 = Label( self.frame2, font=("Courier", 30 , BOLD), style="BW.TLabel", padding=20 )
        text1 = f"OCR Summary"
        self.tf_label2['text'] = text1 
        self.tf_label2.grid(row=1, column=2, columnspan=1, rowspan=1,sticky=tk.N+tk.S+tk.W+tk.E, pady=self.height*0.02, padx=self.width*0.03)


        # main heading
        self.tf_label1 = Label( self.frame2, font=("Courier", 25), style="BW.TLabel", padding=20 )
        self.tf_label1['text']  = "Text 1 = Not Deteced \nText 2 = Not Deteced \nText 3 = Not Deteced \nText 4 = Not Deteced \nText 5 = Not Deteced \nText 6 = Not Deteced \nText 7 = Not Deteced \nText 8 = Not Deteced \nText 9 = Not Deteced"
        self.tf_label1.grid(row=2, column=2, columnspan=1, rowspan=1,sticky=tk.N+tk.S+tk.W+tk.E, pady=self.height*0.02, padx=self.width*0.03)

        
        
        def Button_hover(e):
            style.configure("TButton", foreground="red",
                            background="blue", font=('Helvetica', 22))

        def Button_hover_leave(e):
            style.configure("TButton", foreground="red",
                            background="yellow", font=('Helvetica', 22))

        # self.myBtn = Button(text="Predict", style="TButton" , command=self.update)
        # self.myBtn.bind("<Enter>", Button_hover)

        # self.myBtn.bind("<Leave>", Button_hover_leave)

        # self.myBtn.place(x=self.width/2.35, y=self.height-100)
        # self.myBtn.config(width=8)
        self.delay = 1
        self.frames = 0
        self.callUpdate()
        self.window.mainloop()

########################################################################################################################
    
    def callUpdate(self):
        self.t1Check = False
        self.t1 = threading.Thread(target=self.update).start()
        if self.t1Check:
            self.t1.join()

#########################################################################################################################

    def update(self):
        global ocr_data
        global User_ID
        global Conveyor_ID
        global Status
        final_text=[]
        global nWidth 
        global nHeight
        global nBitCount 
        ard.write(bytes('o','utf-8'))

        libKsj.KSJ_SetParam(0, 1, g_gain)
        libKsj.KSJ_SetParam(0, 2, g_gain)
        libKsj.KSJ_SetParam(0, 3, g_gain)
        libKsj.KSJ_SetParam(0, 4, g_gamma)
        libKsj.KSJ_SetParam(0, 14, g_contrast)
        libKsj.KSJ_SetParam(0, 15, g_brigthness)
        libKsj.KSJ_SetParam(0, 23, g_exposurelines)
        libKsj.KSJ_SetParam(0, 13, 0)
        self.counter+=1
        final_text=[]

###########################################################################################################################
######################################### CAMERA CODE TO CAPTURE STILL IMAGE ##############################################
        g_trigermode = 1
        ret = libKsj.KSJ_TriggerModeSet(0, g_trigermode)
        trigermode = c_int();
        libKsj.KSJ_TriggerModeGet(0, byref(trigermode))
        nbufferSize = nWidth.value * nHeight.value * nBitCount.value / 8
        pRawData = create_string_buffer(int(nbufferSize))
        retValue = libKsj.KSJ_CaptureRgbData(0, pRawData)

        if retValue:
            libKsj.KSJ_EmptyFrameBuffer(0)
            # time.sleep(0.05)
            ard.write(bytes('n','utf-8'))
            time.sleep(1)
            g_trigermode = 0
            ret = libKsj.KSJ_TriggerModeSet(0, g_trigermode)
            nbufferSize = nWidth.value * nHeight.value * nBitCount.value / 8
            pRawData = create_string_buffer(int(nbufferSize))
            retValue = libKsj.KSJ_CaptureRgbData(0, pRawData)
            image = np.frombuffer(pRawData, np.uint8).reshape(nHeight.value, nWidth.value, int(nBitCount.value/8))
            # image=cv2.flip(image,0)
            trigermode = c_int()
            libKsj.KSJ_TriggerModeGet(0, byref(trigermode))
            image= cv2.cvtColor(image,cv2.COLOR_GRAY2BGR)
            image_show=image.copy()
##########################################################################################################################
            today = datetime.datetime.now()
            t = time.strftime("%I-%M-%S%p")
            file_name = today.strftime('%d-%m-%Y') + '__' + t
            date_time=today.strftime('%Y/%m/%d %I:%M:%S')
            cv2.imwrite("output_images/{}.jpg".format(file_name),image)

############################################################################################################################
            t1=time.time()
            img, disp = detect('best_18jan_2022.pt', 640, image) 
            for i in disp:
                # print(i['name'])
                # cv2.imshow('image',i['image'])
                # cv2.waitKey(0)
                # cv2.destroyAllWindows()
                
                check, number = self.class_ocr._OCR(i['image'], i['name'])
                if number!="" and check==True:
                    final_text.append(number) 
                    cv2.rectangle(image_show,(i['xmin'],i['ymin']),(i['xmax'],i['ymax']),(255,0,0),10)

        t2=time.time()
        # print("TOTAL TIME TAKEN: ",t2-t1)
        print("OCR COMPLETED")
        frame = cv2.resize(image_show , (500,500))
        frame = cv2.cvtColor(frame , cv2.COLOR_BGR2RGB)
        self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
        self.canvas.create_image(0,0, image = self.photo, anchor = tk.NW)
        
        mt=""
        for i in range(len(final_text)):
            mt+=f"Text{i+1} = {final_text[i]}\n"
        self.tf_label1['text'] = mt
        final_text=list(map(str,final_text))
        df = pd.DataFrame(data=final_text, columns=["Text Detected"])
        df.to_excel(f'batch_data\{file_name}.xlsx')

############################################################################################################################

        ocr_data=final_text
        Status="Completed"
        
        insert_records = '''INSERT INTO BoxOcrProject.dbo.ocr_project_final(Date_Time,Conveyor_ID,User_ID,OCR_Detected,Status) VALUES(?,?,?,?,?) '''
        
        for index,i in enumerate(ocr_data):
            cursor.execute(insert_records, date_time,Conveyor_ID,User_ID,i,Status)
        conn.commit()
        
        self.window.after(self.delay, self.callUpdate)

#############################################################################################################################

def main():
    root = ThemedTk(theme="breeze")
    root.state('iconic')
    root.resizable(False, False)
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    root.geometry(f"{width}x{height}")
    App(root, "Tkinter and OpenCV" ,  height , width)

#############################################################################################################################

if __name__ == '__main__':
    main()