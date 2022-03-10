import re
from OCR.Paddle_OCR import Paddle_OCR
from OCR.Easy_OCR import Easy_OCR
from OCR.TextReplacement import TextReplacement
from OCR.ImageRotation import ImageRotation 
from OCR.RegularExpression import RegularExpression
from OCR.ImageProccessing import ImageProccessing
import cv2

class _OCR_:

    def __init__(self):
        self._ocrPaddle = Paddle_OCR()
        self._ocrEasy = Easy_OCR()
        self._ImageRotation = ImageRotation()
        self._TextReplacement = TextReplacement()
        self._RegularExpression = RegularExpression()
        self._ImageProccessing = ImageProccessing()

        self.ocrPaddle = self._ocrPaddle.Initialize()
        self.ocrEasy = self._ocrEasy.Initialize()

    
    def _OCR(self, image, className):

        #Image Rotation
        image = self._ImageRotation.rotate_by_class(class_name=className, image=image, pos=['up', 'right', 'down', 'left'])

        #Text Replacement
        def Replacement(text):
            replace = [['o', '0'], ['O','0'], ['Q','0'], ['J', '3'],
                ['i', '1'], ['B', '3'], ['*', ''], ['ot', ' '], ['Lot', ' '], ['lot', ' '], ['Lot:', ' '], ['lot:', ' '],
                 ['T', '7'], ['t','7'], ['Z', '3'], ['z', '3']]
            text = self._TextReplacement.replace_by_list(text=text, lst=replace)
            text = self._TextReplacement.remove(text, flags="alphabet", replace=" ")
            text = self._TextReplacement.remove(text, flags="symbols", replace=" ", symbols="!#$%&'()*-+,.:;<=>?@[]^_`{|}~")
            return text

        def InterpolationText(image):
            image = self._ImageProccessing.Interpolation(image, 1.5, 1.5)
            text = self._ocrPaddle.Details(self.ocrPaddle, image)
            text = Replacement(text)
            return text

        #Get Details
        if self._RegularExpression.String(className,"print_qr")[0] == True:
            orignal_image = image
            image = self._ImageProccessing.Thresholding_By_HSV(image)
            text = self._ocrEasy.Details(self.ocrEasy, image)
            text = Replacement(text)
            check, number = self._RegularExpression.String(text, "\s[0-9+]{4}\s")
            if check==True:
                return check, number
            else:
                alt = [40,70,80,100,125]
                for al in alt:
                    image = self._ImageProccessing.increase_brightness(orignal_image, al)
                    image = self._ImageProccessing.Thresholding_By_HSV(image)
                    text = self._ocrEasy.Details(self.ocrEasy, image)
                    text = Replacement(text)
                    check, number = self._RegularExpression.String(text, "\s[0-9+]{4}\s")
                    if check==True:
                        return check, number
                return False, ""
        
        text = self._ocrPaddle.Details(self.ocrPaddle, image)
        # print("Before: ", text)
        text = Replacement(text)
        # print("After: ", text)
        if self._RegularExpression.String(className, "digit")[0] == True:
            check, number = self._RegularExpression.String(text, "\s[0-9+]{16}\s")
            if check == True:
                return check, number[3:]
            else:
                text = InterpolationText(image)
                check, number = self._RegularExpression.String(text, "\s[0-9+]{16}\s")
                if check == True:
                    return check, number[3:]
                else:
                    return False, ""
        elif self._RegularExpression.String(className, "qrcode")[0] == True:
            text = text[13:]
            check_shade, shade = self._RegularExpression.String(text, "\s[0-9+]{4}\s")
            check_lot, lot = self._RegularExpression.String(text, "\s[0-9+]{10}\s")
            if len(lot) == 10:
                if str(lot[:2]) == '07':
                    lot = lot[2:]
            if check_shade==True and check_lot==True:
                return True, shade + lot
            elif check_shade==True and check_lot==False:
                text = InterpolationText(image)
                text = text[13:]
                check_lot, lot = self._RegularExpression.String(text, "\s[0-9+]{10}\s")
                if len(lot) == 10:
                    if str(lot[:2]) == '07':
                        lot = lot[2:]
                else:
                    check_lot, lot = self._RegularExpression.String(text, "\s[0-9+]{8}\s")
                if check_lot == True:
                    return True, shade + lot
                else:
                    return False, ""
            elif check_shade==False and check_lot==True:
                text = InterpolationText(image)
                text = text[13:]
                check_shade, shade = self._RegularExpression.String(text, "\s[0-9+]{4}\s")
                if check_shade == True:
                    return True, shade + lot
                else:
                    return False, ""
            elif check_shade==False and check_lot==False:
                text = InterpolationText(image)
                text = text[13:]
                check_shade, shade = self._RegularExpression.String(text, "\s[0-9+]{4}\s")
                check_lot, lot = self._RegularExpression.String(text, "\s[0-9+]{10}\s")
                if len(lot) == 10:
                    if str(lot[:2]) == '07':
                        lot = lot[2:]
                else:
                    check_lot, lot = self._RegularExpression.String(text, "\s[0-9+]{8}\s")
                if check_shade==True and check_lot==True:
                    return True, shade + lot
                else:
                    return False, ""
        elif self._RegularExpression.String(className, "barcode")[0] == True:
            check_shade, shade = self._RegularExpression.String(text, "\s[0-9+]{4}\s")
            check_lot_8, lot_8 = self._RegularExpression.String(text, "\s[0-9+]{8}\s")
            check_lot_9, lot_9 = self._RegularExpression.String(text, "\s[0-9+]{9}\s")
            if check_shade==True and (check_lot_8==True or check_lot_9==True):
                return True, shade + lot_8 + lot_9 
            elif check_shade==True and (check_lot_8==False or check_lot_9==False):
                text = InterpolationText(image)
                check_lot_8, lot_8 = self._RegularExpression.String(text, "\s[0-9+]{8}\s")
                check_lot_9, lot_9 = self._RegularExpression.String(text, "\s[0-9+]{9}\s")
                if (check_lot_8 == True or check_lot_9==True):
                    return True, shade + lot_8 + lot_9
                else:
                    return False, ""
            elif check_shade==False and (check_lot_8==True or check_lot_9==True):
                text = InterpolationText(image)
                check_shade, shade = self._RegularExpression.String(text, "\s[0-9+]{4}\s")
                if check_shade == True:
                    return True, shade + lot_8 + lot_9
                else:
                    return False, ""
            elif check_shade==False and (check_lot_8==False or check_lot_9==False):
                text = InterpolationText(image)
                check_shade, shade = self._RegularExpression.String(text, "\s[0-9+]{4}\s")
                check_lot_8, lot_8 = self._RegularExpression.String(text, "\s[0-9+]{8}\s")
                check_lot_9, lot_9 = self._RegularExpression.String(text, "\s[0-9+]{9}\s")
                if check_shade==True and (check_lot_8==True or check_lot_9==True):
                    return True, shade + lot_8 + lot_9
                else:
                    return False, ""
        else:
            return False, ""

