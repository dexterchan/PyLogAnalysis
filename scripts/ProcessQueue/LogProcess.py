'''
Created on Jan 29, 2017

@author: dexter
'''
from Models.LogMessage import *
from Models.ProdIssueIncidentModel import *
from collections import deque
import logging
logger = logging.getLogger("")

class LogQueuePublisher:
    def __init__(self, publisher):
        '''
        Constructor
        '''
        self.publisher=publisher
        self.myQueue = deque()
        return
    
    
    def queueIssue(self, logMessage):
        self.myQueue.append(logMessage)
        logger.info(logMessage.toString())
        return
    def dequeueIssue(self):
        M= self.myQueue.popleft()
        return M


class LogClassReportExtractor:
    def __init__(self, ntl_OneNNcluserInstance,incidentTicketServiceImpl):
        '''
        Constructor
        '''
        self.ntl_OneNNcluserInstance=ntl_OneNNcluserInstance
        self.incidentTicketServiceImpl=incidentTicketServiceImpl
        
        return
    
    def extractLogClassSolution(self,logM):
        logAlert = {}
        logAlert["ORGMSG"] = logM.MESSAGE
        logAlert["ISO_DATE"]=logM.ISO_DATE
        logAlert["STATUS"]=logM.STATUS
        logAlert["LogClass"] = logM.ClassName
        if(logM.ClassName is  None):
            cName = self.ntl_OneNNcluserInstance.identifyCluster(Sentence(logM.MESSAGE))
            logM.ClassName=cName
        if(logM.ClassName is not None):
            if(logM.ClassName in self.incidentTicketServiceImpl.ProdIssue2IncidentMap.keys()):
                incidentList = self.incidentTicketServiceImpl.ProdIssue2IncidentMap[logM.ClassName]
                logAlert["relatedIncident"]=[]
                for incident in incidentList:
                    logAlert["relatedIncident"].append(self.incidentTicketServiceImpl.incidentTicketMap [incident].__dict__)
        
        return logAlert