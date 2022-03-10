import numpy as np
import re

class ImageRotation:
    def __init__(self):
        pass

    @staticmethod
    def rotate_by_position(image, pos = -1):
        '''
        Rotate Image

        :param image image: pass image
        :param integer pos: pass position for `top` pos=0, `right` pos=1, `bottom` pos=2, `left` pos=3
        '''
        try:
            if pos == 0:
                return np.rot90(image, 0)
            elif pos == 1:
                return np.rot90(image, 1)
            elif pos == 2:
                return np.rot90(image, 2)
            elif pos == 3:
                return np.rot90(image, 3)
        except:
            raise "Image Rotation Error: By Position"

    @staticmethod
    def rotate_by_class(class_name, image, pos):
        '''
        Rotate Iamge
        
        :param str class_name: Annotated Class name = `class_name1_top`, `class_name1_right`, `class_name1_bottom`, `class_name1_left`
        :param image image: pass image
        :param array pos: pos argument like this `['up', 'right', 'down', 'left']`
        '''
       
        try:
            position = lambda p: bool(re.findall(p, class_name))
            if position(pos[1]) == True:
                return np.rot90(image, 1)
            elif position(pos[2]) == True:
                return np.rot90(image, 2)
            elif position(pos[3]) == True:
                return np.rot90(image, 3)
            elif position(pos[0]) == True:
                return image
        except:
            raise "Image Rotation Error: By Class "