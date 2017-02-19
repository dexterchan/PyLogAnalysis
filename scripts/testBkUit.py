'''
Created on Feb 19, 2017

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



def testSubmitLogWorkflowWithBk():
    
    
    
    classifier = ntl_OneNNcluser()
    classifier.loadModel("./modelBackup.json")
    
    
    
    
    incidentService = IncidentTicketService()
    testIncident = IncidentTicket("123","NEW")
    testIncident.errorLog="FxRestfulController: UAEIPT not found: unknown"
    incidentService.addNewIncident(testIncident,classifier)
    
    testIncident = IncidentTicket("456","NEW")
    testIncident.errorLog="FxRestfulController: USDUSD not found: ccy1 and ccy2 should not be the same FxRestfulController.java 208"
    incidentService.addNewIncident(testIncident,classifier)
    
    
    
    logM = LogMessage()
    
    logM.STATUS = "ERROR"
    logM.MESSAGE = "FxRestfulController: EUREUR not found: ccy1 and ccy2 should not be the same FxRestfulController.java 208"
    logM.ISO_DATE = "2016-12-30 16:27:54,435"
    newdata = Sentence(logM.MESSAGE)
    #logM.ClassName=classifier.identifyCluster(newdata)
    
    logM.ClassName=classifier.identifyCluster(newdata)
    
    logClass = LogClassReportExtractor(classifier, incidentService)
    result= logClass.extractLogClassSolution(logM)
    logger.info(json.dumps(result))
    
    logPublisher = LogQueuePublisher(None)
    logPublisher.start()
    logPublisher.queueIssue(result)
    
    
    
    return




testSubmitLogWorkflowWithBk()