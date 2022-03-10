import easyocr

class Easy_OCR():
    def __init__(self):
      pass

    @staticmethod
    def Initialize(gpu = True):
        return easyocr.Reader(['en'], gpu=gpu)

    @staticmethod
    def Details(reader, image):
        text = ""
        result = reader.readtext(image) 
        for detection in result: 
            text += detection[1] + " "
        text = " " + text + " "
        return text
