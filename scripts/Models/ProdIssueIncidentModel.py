'''
Created on Jan 29, 2017

@author: dexter
'''

from Classifier.ntl_OneNNcluster import ntl_OneNNcluser
from  Models.SentenceModel import Sentence
import logging
logger = logging.getLogger("")
import json
import copy
import pprint
class IncidentTicket:
    '''
    a class for sentence analysis
    '''

    def __init__(self, incidentId,status):
        '''
        Constructor
        '''
        self.incidentId=incidentId
        self.status=status
        self.errorLog=""
        self.causeAnalysis=""
        self.solution=""
    

class IncidentTicketService:
    
    def __init__(self):
        self.incidentTicketMap={}
        self.ProdIssue2IncidentMap={}
        self.Incident2ProdIssueMap={}
    
    def toMap(self):
        myCopy={}
        
        incidentMap={}
        for s in self.incidentTicketMap.values():
            incidentMap[s.incidentId] = s.__dict__
        myCopy["incidentTicketMap"]=incidentMap
        myCopy["ProdIssue2IncidentMap"] = self.ProdIssue2IncidentMap
        myCopy["Incident2ProdIssueMap"]=self.Incident2ProdIssueMap
        return myCopy
    
    def saveModel(self, IncidentBackupFile):
        m = self.toMap()
        with open(IncidentBackupFile, 'w') as fp:
            json.dump(m, fp)
        return
    def loadModel(self, IncidentBackupFile):
        
        with open(IncidentBackupFile,'r') as fr:
            data = json.load(fr)
        #pprint(data)
        
        self.incidentTicketMap = {}
        for s in data["incidentTicketMap"].values():
            incidentId = s["incidentId"]
            status = s["status"]
            incTicket = IncidentTicket(incidentId,status)
            incTicket.errorLog = s["errorLog"]
            incTicket.causeAnalysis=s["causeAnalysis"]
            incTicket.solution=s["solution"]
            self.incidentTicketMap[incidentId] = incTicket
        
        self.ProdIssue2IncidentMap = data["ProdIssue2IncidentMap"]
        self.Incident2ProdIssueMap = data["Incident2ProdIssueMap"]
        return
    
    def addNewIncident(self, newIncident,classifier):
        #register new incident into storage
        #try to map into cluster
        #if fail to map to cluster, add a new instance in cluster
        logger.debug(newIncident.incidentId + newIncident.errorLog)
        if (newIncident.incidentId in self.incidentTicketMap.keys()):
            self.updateIncidentTicket( newIncident)
            
            return self.Incident2ProdIssueMap[newIncident.incidentId]
        #insert new incident now
        self.incidentTicketMap[newIncident.incidentId] = newIncident
        
        cName = self.associateIncident2Cluster(newIncident,classifier)
        
        return cName
    
    def updateIncidentTicket(self,oldIncident):
        #update existing incident 
        self.incidentTicketMap[oldIncident.incidentId] = oldIncident
        return
    
    def associateIncident2Cluster(self, newIncident,classifier):
        #check classifier
        self.Incident2ProdIssueMap[newIncident.incidentId]=""
        ErrorLogSentence = Sentence(newIncident.errorLog)
        cName=classifier.identifyCluster(ErrorLogSentence)
        
        if(cName is None):
            #new issue and created new classifier
            cName=classifier.identifyCluster(ErrorLogSentence)
        
        if(cName is not None):
            if(cName not in self.ProdIssue2IncidentMap.keys() ):
                self.ProdIssue2IncidentMap[cName]=[]
            self.ProdIssue2IncidentMap[cName].append(newIncident.incidentId)
        else:
            raise "Failed to create map new incident"
        self.Incident2ProdIssueMap[newIncident.incidentId]=cName
        return cName