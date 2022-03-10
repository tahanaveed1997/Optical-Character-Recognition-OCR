import re

from pandas import array

class TextReplacement:
    def __init__(self):
        pass

    @staticmethod
    def replace_by_list(text, lst):
        '''
        Replace Text by list

        :param str text: pass string
        :param list lst: pass list like this [['o', '0'], ['O', '0']]
        '''
        try:
            for l in lst:
                text = text.replace(str(l[0]), str(l[1]))
            return text
        except:
            raise "Error: Replace text list: " + str(lst)

    @staticmethod
    def replace_by_dict(text, dict):
        '''
        Replace Text by dictionary

        :param str text: pass string
        :param dictionary dict: pass dictionary like this {" key1" : [['o', '0'], ['O', '0']], "key2" : [['o', '0'], ['O', '0']]}
        '''
        try:
            for key, value in dict.items():
                for v in value:
                    for l in v:
                        text = text.replace(str(l[0]), str(l[1]))
            return text
        except:
            raise "Error: Replace text dictionary: " + dict
    
    @staticmethod
    def remove(text, flags="", replace="", symbols = ""):
        '''
        Remove values as per your requirment

        :param str text: pass string
        :param str flags: for removing numbers use "numeric" argument in single or duble quotes
        :param str flags: for removing alphabets use "alphabet" argument in single or duble quotes
        :param str flags: for removing symbols use "symbols" argument in single or duble quotes
        :param str replace: for removing text-raplacement use space " "  
        :param str symbols: for removing symbols use like this "!"#$%&\'()*+,-./:;<=>?@[]^_`{|}~"
        '''
        if flags!="":
            if flags=="numeric":
                return re.sub("[^a-zA-Z]", replace, text)
            elif flags=="alphabet":
                return re.sub("[^0-9]", replace, text)
            elif flags=="symbols":
                return text.translate({ ord(c): None for c in symbols })
        else:
            raise "Error: Pass flag value in remove function."
        

