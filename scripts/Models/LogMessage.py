'''
Created on Jan 30, 2017

@author: dexter
'''
class LogMessage:
    def __init__(self):
        '''
        Constructor
        '''
        self.STATUS=""
        self.MESSAGE = ""
        self.ISO_DATE=""
        self.ClassName=None
        return
    
    def toString(self):
        report={}
        report["STATUS"] = self.STATUS
        report["MESSAGE"]=self.MESSAGE
        report["ISO_DATE"]=self.ISO_DATE
        report["ClassName"]=self.ClassName
        
        return