import re

text1="12"

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


print(String(text1,"[0-9]|[0-9]|[0-9]"))
# print(String(text1,"[0-9]{2}[.][0-9]{2}"))