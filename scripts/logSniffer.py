'''
Created on Jan 14, 2017

@author: dexter
'''
from Setting.LogToken import  *
import re
import logging




class LogSniffer:
    #logPattern is an text array of STATUS,ISO_DATE,MESSAGE,SEPARATOR
    
    def __init__(self, logPattern,classifier):
        '''
        Constructor
        '''
        logging.basicConfig(level=logging.DEBUG)
        #self.logger = logging.getLogger()
        #self.logger.setLevel(logging.DEBUG)
        self.initialized=False
        self.trainingData=[]
        self.RegexPattern=""
        self.classifier=classifier
        self.logPattern=logPattern
        self.setLogRegex()
        
        
    def setLogRegex(self):
        if(len(self.logPattern)>0):
            self.RegexPattern=LogTokenRegexPattern[self.logPattern[0] ]
        for i in range(1, len(self.logPattern)):
            self.RegexPattern=self.RegexPattern + LogTokenRegexPattern["SEPARATOR"]+LogTokenRegexPattern[self.logPattern[i] ] 
        
        return

    
    def setupModelFromLogFile(self,logFileName,StatusInterested):
        with open(logFileName) as f:
            content = f.readlines()
        
        
        for st in content:
            matchObj=re.match(self.RegexPattern, st)
            
            if matchObj:
                logDict={}
                for inx in range (0,len(self.logPattern)):
                    logDict[ self.logPattern[inx] ] = matchObj.group(inx+1)
                
                if("STATUS" in logDict and "MESSAGE" in logDict):
                    if(logDict["STATUS"] == "ERROR"):
                        self.classifier.InsertData(logDict["MESSAGE"])
        m=self.classifier.buildModelFromTrainingData1D()
        logging.info("Model trained with "+str(len(self.classifier.trainingData)))
        
        
        return