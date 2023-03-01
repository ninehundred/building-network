import re

def strip(string_in):
    """strips string to prepare for conversion into (x,y) float pair"""
    return re.sub("[a-z]|[A-Z]|[A-Z]|[a-z]|[=]|[\s]|[(]|[)]", "", string_in)
