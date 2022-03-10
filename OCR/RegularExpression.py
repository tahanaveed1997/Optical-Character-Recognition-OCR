import re

class RegularExpression:
    def __init__(self):
        pass

    @staticmethod
    def String(text, expression):
        '''
        Find String 

        :param str text: pass text
        :param str expression: pass expression for four digits like this "\s[0-9+]{4}\s"
        '''
        try:
            return True, str(re.findall(expression, text)[0].strip())
        except:
            return False, ""

    @staticmethod
    def StringSearch(text, expression):
        try:
            return True, re.search(expression, text)[0]
        except:
            return False, ""
