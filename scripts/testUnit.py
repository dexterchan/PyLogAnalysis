'''
Created on Jan 14, 2017

@author: dexter
'''
from Classifier.ntl_OneNNcluster import ntl_OneNNcluser 
from logSniffer import *
import argparse
from  Models.SentenceModel import Sentence

from Models.ProdIssueIncidentModel import *

from Models.LogMessage import *
from ProcessQueue.LogProcess import  *

import logging
import logging.handlers
import json

LOGFILE = "Testing.log"
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s (%(threadName)-2s) %(message)s',
                    )
logger = logging.getLogger("")
logger.setLevel(logging.DEBUG)
handler = logging.handlers.RotatingFileHandler(
    LOGFILE, maxBytes=(1048576*5), backupCount=7
)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

parser = argparse.ArgumentParser(__file__, description="NLTK tester")

parser.add_argument("--trainsample", "-s", dest='trainSampleFile', help="Input a training sample file" )
parser.add_argument("--output", "-o", dest='outputFile', help="Write log to output file")
parser.add_argument("--modelfile", "-m", dest='modelfile', help="input by model file")
parser.add_argument("--incidentfile", "-i", dest='incidentfile', help="input by incident file")

args = parser.parse_args()
fname=args.trainSampleFile
oFile=args.outputFile
modelFile=args.modelfile

def PrintModel(m):
    
    return

def testSentenceDataInsert():
    classifier = ntl_OneNNcluser("file.txt")
    classifier.InsertData("ERROR 2016-12-31 18:39:40,268 - FxRestfulController: JPYJPY not found: ccy1 and ccy2 should not be the same FxRestfulController.java 64 ")
    classifier.InsertData('ERROR 2016-12-30 16:27:54,435 - FxRateUpdaterThread: org.springframework.web.client.ResourceAccessException: I/O error on GET request for "http://www.apilayer.ne/api/live": www.apilayer.ne: nodename nor servname provided, or not known; nested exception is java.net.UnknownHostException: www.apilayer.ne: nodename nor servname provided, or not known FxRateUpdaterThread.java 88')
    
    m=classifier.buildModelFromTrainingData1D()
    print (m) 
    return

def testLogSniffer(fileName,oFile):
    pattern = ["ISO_DATE","STATUS","MESSAGE"]
    StatusInterested = ["ERROR"]
    
    classifier = ntl_OneNNcluser()
    logSniffer = LogSniffer(pattern,classifier)
    
    logSniffer.setupModelFromLogFile(fileName, StatusInterested)
    classifier.printModel(oFile)
    
    classifier.saveModel(modelFile)
    
    return

def testLoadModel(filename, data):
    classifier = ntl_OneNNcluser()
    classifier.loadModel(filename)
    
    q=classifier.identifyCluster(Sentence(data))
    print (q)
    
    classifier.saveModel("./newModel.json")
    
    return

def testIncidentTicket():
    classifier = ntl_OneNNcluser()
    classifier.loadModel("./modelBackup.json")
    
    testIncident = IncidentTicket("123","NEW")
    testIncident.errorLog="FxRestfulController: UAEIPT not found: unknown"
    incidentService = IncidentTicketService()
    incidentService.addNewIncident(testIncident,classifier)
    
    
    testIncident = IncidentTicket("123","NEW")
    testIncident.errorLog="FxRestfulController: UAEIPT not found: unknown"
    testIncident.solution="add ccy"
    incidentService.addNewIncident(testIncident,classifier)
    incidentService = incidentService
    
    return



def testSubmitLogWorkflow2():
    classifier = ntl_OneNNcluser()
    classifier.loadModel("./modelBackup.json")
    
    logM = LogMessage()
    
    logM.STATUS = "ERROR"
    logM.MESSAGE = "FxRestfulController: EUREUR not found: ccy1 and ccy2 should not be the same FxRestfulController.java 208"
    logM.ISO_DATE = "2016-12-30 16:27:54,435"
    newdata = Sentence(logM.MESSAGE)
    #logM.ClassName=classifier.identifyCluster(newdata)
    logPublisher = LogQueuePublisher(None)
    logPublisher.queueIssue(logM)
    
    
    incidentService = IncidentTicketService()
    testIncident = IncidentTicket("123","NEW")
    testIncident.errorLog="FxRestfulController: UAEIPT not found: unknown"
    incidentService.addNewIncident(testIncident,classifier)
    
    testIncident = IncidentTicket("456","NEW")
    testIncident.errorLog="FxRestfulController: USDUSD not found: ccy1 and ccy2 should not be the same FxRestfulController.java 208"
    incidentService.addNewIncident(testIncident,classifier)
    
    logClass = LogClassReportExtractor(classifier, incidentService)
    result= logClass.extractLogClassSolution(logM)
    logger.info(json.dumps(result))
    return

def saveIncidentMap():
    classifier = ntl_OneNNcluser()
    classifier.loadModel("./modelBackup.json")
    incidentService = IncidentTicketService()
    testIncident = IncidentTicket("123","NEW")
    testIncident.errorLog="FxRestfulController: UAEIPT not found: unknown"
    incidentService.addNewIncident(testIncident,classifier)
    
    testIncident = IncidentTicket("456","NEW")
    testIncident.errorLog="FxRestfulController: USDUSD not found: ccy1 and ccy2 should not be the same FxRestfulController.java 208"
    incidentService.addNewIncident(testIncident,classifier)
    
    
    testIncident = IncidentTicket("987","NEW")
    testIncident.errorLog="FxRestfulController: DKKJPY not found: Graph must contain the end vertex! FxRestfulController.java 64"
    incidentService.addNewIncident(testIncident,classifier)
    
    incidentService.saveModel("./IncidentBackup.json")
    
    incidentService2 = IncidentTicketService()
    incidentService2.loadModel("./IncidentBackup.json")
    
    return

from ProcessQueue.LogPublisher import  *
def testSubmitLogWorkflowFinal():
    classifier = ntl_OneNNcluser()
    classifier.loadModel("./modelBackup.json")
    
    logM = LogMessage()
    
    logM.STATUS = "ERROR"
    logM.MESSAGE = "UAE/IPR not found: Graph must contain the end vertex!"
    logM.ISO_DATE = "2016-12-30 16:27:54,435"
    newdata = Sentence(logM.MESSAGE)
    #logM.ClassName=classifier.identifyCluster(newdata)
    logPublisher = LogQueuePublisher(None)
    logPublisher.queueIssue(logM)
    
    
    incidentService = IncidentTicketService()
    testIncident = IncidentTicket("123","NEW")
    testIncident.errorLog="FxRestfulController: UAEIPT not found: unknown"
    incidentService.addNewIncident(testIncident,classifier)
    
    testIncident = IncidentTicket("456","NEW")
    testIncident.errorLog="FxRestfulController: USDUSD not found: ccy1 and ccy2 should not be the same FxRestfulController.java 208"
    incidentService.addNewIncident(testIncident,classifier)
    
    testIncident = IncidentTicket("987","NEW")
    testIncident.errorLog="FxRestfulController: DKKJPY not found: Graph must contain the end vertex! FxRestfulController.java 64"
    incidentService.addNewIncident(testIncident,classifier)
    
    logClass = LogClassReportExtractor(classifier, incidentService)
    result= logClass.extractLogClassSolution(logM)
    logger.info(json.dumps(result))
    
    p=RestfulPublisher("http://ec2-52-66-21-39.ap-south-1.compute.amazonaws.com/postlog")

    (response,content)=p.publish(result)
    logger.info (response) 
    logger.info (content) 
    
    return


fileName="/Users/dexter/TravelFxConvert/TravelFxConvertCore/logs/TravelFxConvertRestful.log"
if (fname is not None):
    fileName=fname
#testLogSniffer(fileName,oFile)
#testLoadModel("./modelBackup.json","FxRestfulController: UAEIPT not found: unknown")
#testSentenceDataInsert()

#testIncidentTicket()
#saveIncidentMap()
#testSubmitLogWorkflow2()
testSubmitLogWorkflowFinal()
