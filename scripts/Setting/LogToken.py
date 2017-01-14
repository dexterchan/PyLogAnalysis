'''
Created on Jan 14, 2017

@author: dexter
'''
#(.*?)\s*?(\d{4}-\d{2}-\d{2}[\s\t]*?\d{2}:\d{2}:\d{2}[\,\.]*?\d{3})\s*?(.*?$)

LogTokenRegexPattern = {
    "STATUS":"(.*?)",
    "ISO_DATE": "(\d{4}-\d{2}-\d{2}[\s\t]*?\d{2}:\d{2}:\d{2}[\,\.]*?\d{3})",
    "MESSAGE":"(.*?$)",
    "SEPARATOR":"\s*?"
}