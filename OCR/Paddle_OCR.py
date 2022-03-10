from paddleocr import PaddleOCR, draw_ocr #OCR

class Paddle_OCR():
  
  def __init__(self):
      pass
  
  @staticmethod
  def Initialize(gpu=True):
    ''' 
    For GPU Use this parameter "gpu=True"
    '''
    return PaddleOCR(use_angle_cls=True, lang='en', use_gpu=gpu)

  @staticmethod
  def Details(ocr, image):
    ''' 
    Return String  
    '''
    result = ocr.ocr(image, cls=True)
    lst = [res[1][0] for res in result]
    text = ' '.join([str(elem) for elem in lst])
    text = " " + text + " "
    return text
