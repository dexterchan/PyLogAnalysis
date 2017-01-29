'''
Created on Jan 29, 2017

@author: dexter
'''

from Classifier.ntl_OneNNcluster import ntl_OneNNcluser
from  Models.SentenceModel import Sentence
import logging
logger = logging.getLogger("")

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
        self.solution=""
    

class IncidentTicketService:
    
    def __init__(self,ntl_OneNNcluserInstance):
        self.incidentTicketMap={}
        self.ProdIssue2IncidentMap={}
        self.Incident2ProdIssueMap={}
        self.cluster = ntl_OneNNcluserInstance
    
    def addNewIncident(self, newIncident):
        #register new incident into storage
        #try to map into cluster
        #if fail to map to cluster, add a new instance in cluster
        logger.debug(newIncident.incidentId + newIncident.errorLog)
        if (newIncident.incidentId in self.incidentTicketMap.keys()):
            self.updateIncidentTicket( newIncident)
            
            return self.Incident2ProdIssueMap[newIncident.incidentId]
        #insert new incident now
        self.incidentTicketMap[newIncident.incidentId] = newIncident
        
        cName = self.associateIncident2Cluster(newIncident)
        
        return cName
    
    def updateIncidentTicket(self,oldIncident):
        #update existing incident 
        self.incidentTicketMap[oldIncident.incidentId] = oldIncident
        return
    
    def associateIncident2Cluster(self, newIncident):
        #check cluster
        self.Incident2ProdIssueMap[newIncident.incidentId]=""
        ErrorLogSentence = Sentence(newIncident.errorLog)
        cName=self.cluster.identifyCluster(ErrorLogSentence)
        
        if(cName is None):
            #new issue and created new cluster
            cName=self.cluster.identifyCluster(ErrorLogSentence)
        
        if(cName is not None):
            if(cName not in self.ProdIssue2IncidentMap.keys() ):
                self.ProdIssue2IncidentMap[cName]=[]
            self.ProdIssue2IncidentMap[cName].append(newIncident.incidentId)
        else:
            raise "Failed to create map new incident"
        self.Incident2ProdIssueMap[newIncident.incidentId]=cName
        return cName