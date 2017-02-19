'''
Created on Jan 29, 2017

@author: dexter
'''
from Models.LogMessage import *
from Models.ProdIssueIncidentModel import *
from collections import deque
import threading
from Queue import *

import logging
logger = logging.getLogger("")



#===============================================================================
# class LogBgWork (threading.Thread):
#     def __init__(self, ReportWebSite):
#         '''
#         Constructor
#         '''
#         threading.Thread.__init__(self)
#         self.logQueue=Queue()
#         self.reportWebSite = ReportWebSite
#         self.RunStatus=True
#         return
#     
#     def run(self):
#         
#         while(self.RunStatus):
#             log = self.logQueue.get()
#             logger.info("Dequeue a new log")
#             self.processLog(log)
#         return
#     
#     def insertLog(self, log):
#         self.logQueue.put(log)
#         
#         return
#     
#     def processLog(self, log):
#         logger.info(log)
#         
#         return
#===============================================================================
class LogQueuePublisher(threading.Thread):
    def __init__(self, publisher):
        '''
        Constructor
        '''
        self.publisher=publisher
        threading.Thread.__init__(self)
        self.logQueue=Queue()
        
        self.RunStatus=True
        return
    
    def run(self): 
        while(self.RunStatus):
            log = self.logQueue.get()
            logger.info("Dequeue a new log")
            self.processLog(log)
        return
    
    def queueIssue(self, logMessage):
        self.logQueue.put(logMessage)
        logger.info(logMessage)
        return
    
    def processLog(self, log):
        logger.info(log)
        if (self.publisher is not None):
            self.publisher.publish(log)
        return


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
        
        if(logM.ClassName is  None):
            cName = self.ntl_OneNNcluserInstance.identifyCluster(Sentence(logM.MESSAGE))
            logM.ClassName=cName
        if(logM.ClassName is not None):
            if(logM.ClassName in self.incidentTicketServiceImpl.ProdIssue2IncidentMap.keys()):
                incidentList = self.incidentTicketServiceImpl.ProdIssue2IncidentMap[logM.ClassName]
                logAlert["relatedIncident"]=[]
                for incident in incidentList:
                    logAlert["relatedIncident"].append(self.incidentTicketServiceImpl.incidentTicketMap [incident].__dict__)
        logAlert["LogClass"] = logM.ClassName
        return logAlert