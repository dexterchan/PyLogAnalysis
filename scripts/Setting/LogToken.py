'''
Created on Jan 14, 2017

@author: dexter
'''
#(\\d{4}-\\d{2}-\\d{2}[\\s\t]*?\\d{2}:\\d{2}:\\d{2}[\\,\\.]*?\\d{3})[\\s\\-\\:]*([A-Za-z0-9]+)[\\s\\-\\:]*(.*?$)

LogTokenRegexPattern = {
    "STATUS":"([A-Za-z0-9]+)",
    "ISO_DATE": "(\d{4}-\d{2}-\d{2}[\s\t]*?\d{2}:\d{2}:\d{2}[\,\.]*?\d{3})",
    "MESSAGE":"(.*?$)",
    "SEPARATOR":"[\s\-\:]*"
}