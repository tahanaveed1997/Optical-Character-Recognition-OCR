import os
from os import listdir
from cv2 import imshow
from paddle import crop
from paddleocr import PaddleOCR,draw_ocr
import cv2
import numpy as np
import re

ocr = PaddleOCR(use_angle_cls=True, lang='en',use_gpu=False) # need to run only once to download and load model into memory


def remove(text, flags="", replace="", symbols = ""):
        if flags!="":
            if flags=="numeric":
                return re.sub("[^a-zA-Z]", replace, text)
            elif flags=="alphabet":
                return re.sub("[^0-9]", replace, text)
            elif flags=="symbols":
                return text.translate({ ord(c): None for c in symbols })
        else:
            raise "Error: Pass flag value in remove function."

       
def String(text, expression):
    try:
        return True, str(re.findall(expression, text)[0].strip())
    except:
        return False, ""



def pdf_1(s): 
    quantity_list=[]
    price_list=[]
    count=0
    str1 = "" 
    
    for ele in s: 
        check,code=String(ele,"[A-Z|a-z]{2}[-][0-9]{4}")
        if check==False:
            str1 += ele
            str1+='\n'
        if check==True:
            count+=1
            print("PRODUCT CODE: ",code)  

    if count==0:
        for ele in s:
            check,price=String(ele,"[0-9]{2}[.][0-9]{2}")
            if check==True:
                price_list.append(float(price))
            else:
                ele=remove(ele, flags="alphabet", replace='')
                try:
                    quantity_list.append(int(ele))
                except:
                    pass
        quantity_list.sort(reverse=True)
        price_list.sort(reverse=False)
        print("PRODUCT QUANTITY: ",quantity_list)
        print("PRODUCT PRICE: ",price_list)

    else:
        print("PRODUCT NAME:",s[0]+' '+s[1])
        print("PRODUCT DESCRIPTION:\n",str1)



if __name__ == '__main__':
    image=cv2.imread('pdf_1_images/page10.jpg')
    image=cv2.resize(image,(1100,1100))
    showCrosshair = False
    fromCenter = False
    text_found=[]
    check=False

    ############## CODE FOR PDF1 TEXT EXTRACTION ######################################################
    for i in range(0,2):
        r = cv2.selectROI(image,showCrosshair)
        crop_img = image[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
        crop_img=cv2.resize(crop_img, None, fx = 2, fy = 2, interpolation = cv2.INTER_CUBIC)
        result = ocr.ocr(crop_img, cls=True)
        boxes = [line[0] for line in result]
        txts = [line[1][0] for line in result]
        text=pdf_1(txts)
