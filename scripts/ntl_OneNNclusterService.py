'''
Created on Jan 14, 2017

@author: dexter
'''

import os
import sys
from flask import abort
from flask import jsonify
from flask import make_response
import json
from flask import Flask, request, redirect, send_from_directory,Response
from werkzeug import secure_filename
import logging
import logging.handlers


from Models.SystemStatus import *
from Models.LogMessage import *
from Classifier.ntl_OneNNcluster import ntl_OneNNcluser 
from logSniffer import *
import argparse
from Models.SentenceModel import Sentence
from Models.ProdIssueIncidentModel import *

from Models.LogMessage import *
from ProcessQueue.LogProcess import  *
# Initialize the Flask application
app = Flask(__name__, static_url_path='/static')

LOGFILE = "runClusterService.log"
#logging.basicConfig(level=logging.DEBUG,
#                    format='%(asctime)s (%(threadName)-2s) %(message)s',
#                    )
logger = logging.getLogger("")
logger.setLevel(logging.DEBUG)
handler = logging.handlers.RotatingFileHandler(
    LOGFILE, maxBytes=(1048576*5), backupCount=7
)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

def initialModel(sampleInputFile,oFile,modelFile,incidentfile):
    global classifier
    pattern = ["ISO_DATE","STATUS","MESSAGE"]
    StatusInterested = ["ERROR","WARN"]
    
    classifier = ntl_OneNNcluser()
    if(sampleInputFile is not None):
        logSniffer = LogSniffer(pattern,classifier)
        logSniffer.setupModelFromLogFile(sampleInputFile, StatusInterested)
        classifier.saveModel(modelFile)
    else:
        classifier.loadModel(modelFile)
        
    classifier.printModel(oFile)
    app.config["CLASSIFIER"]=classifier
    incidentService = IncidentTicketService()
    if(incidentfile is not None):
        incidentService.loadModel(incidentfile)
    app.config["INCIDENTSERVICE"]=incidentService
    
    logQPublisher = LogQueuePublisher(None)
    app.config["LogQueuePublisher"]=logQPublisher
    
    
    logClassExtractor = LogClassReportExtractor(classifier, incidentService)
    app.config["LogClassExtractor"]=logClassExtractor
    
    
    return
parser = argparse.ArgumentParser(__file__, description="NLTK tester")

parser.add_argument("--trainsample", "-s", dest='trainSampleFile', help="Input a training sample file" )
parser.add_argument("--output", "-o", dest='outputFile', help="Write log to output file")
parser.add_argument("--modelfile", "-m", dest='modelfile', help="input by model file")
parser.add_argument("--incidentfile", "-i", dest='incidentfile', help="input by incident file")

args = parser.parse_args()
fname=args.trainSampleFile
oFile=args.outputFile
modelFile=args.modelfile
incidentfile=args.incidentfile
    
fileName="output1DCluster.txt"
if (oFile is None):
        oFile=fileName
#if ( fname is None):
#        logging.error("No initial error log sample file in parameter --input")
        
initialModel(fname,oFile,modelFile, incidentfile)

@app.route('/dumpModel', methods=['GET'])
def dumpModel():
    m = classifier.toMap()
    r=Response(json.dumps(m),  mimetype='application/json')
    r.headers['Access-Control-Allow-Origin'] = '*'
    return r


@app.route('/getSystemStatus', methods=['GET'])
def getSystemStatus():
    LogAnalyzeStatus["NumCluster"] = len(classifier.clusterSet)
    #add header "Access-Control-Allow-Origin"
    r = Response(json.dumps(LogAnalyzeStatus),  mimetype='application/json')
    r.headers['Access-Control-Allow-Origin'] = '*'
    return r


@app.route('/submitlog', methods=['POST'])
def submitLog():
    #check request is a json
    if not request.json:
        abort(400)
    classifier=app.config["CLASSIFIER"]
    
    reqMap = request.json
    newdata = Sentence(reqMap["MESSAGE"])
    newdata.init()
    
    logM = LogMessage()
    if ("STATUS" in reqMap.keys() ):
        logM.STATUS = reqMap["STATUS"]
    else:
        abort(402)
    if ("MESSAGE" in reqMap.keys() ):
        logM.MESSAGE = reqMap["MESSAGE"]
    else:
        abort(402)
    if ("ISO_DATE" in reqMap.keys() ):
        logM.ISO_DATE = reqMap["ISO_DATE"]
    else:
        abort(402)
    
    logM.ClassName=classifier.identifyCluster(newdata)
    app.config["LogQueuePublisher"].queueIssue(logM)
    StatusResult={}
    LogAnalyzeStatus["TodayNumIssue"]=LogAnalyzeStatus["TodayNumIssue"]+1
    if(logM.ClassName is not None):
        StatusResult["found"]=True
        StatusResult["cluster"]=logM.ClassName
    else:
        StatusResult["found"]=False
        StatusResult["cluster"]="NoClass"
        LogAnalyzeStatus["TodayUnknownIssue"]=LogAnalyzeStatus["TodayUnknownIssue"]+1
    r = Response(json.dumps(StatusResult),  mimetype='application/json')
    
    r.headers['Access-Control-Allow-Origin'] = '*'
    return r

@app.route('/submitIncident', methods=['POST'])
def submitIncident():
    #check request is a json
    if not request.json:
        abort(400)
    reqMap = request.json
    #self.incidentId
    #    self.status=status
    #    self.errorLog=""
    #    self.solution=""
    if("incidentId" not in reqMap):
        abort(401)
    else:
        incidentId = reqMap["incidentId"]
    
    if("status" not in reqMap):
        abort(401)
    else:
        status = reqMap["status"]
    
    incTicket = IncidentTicket(incidentId,status)
    if("errorLog"  in reqMap):
        incTicket.errorLog = reqMap["errorLog"]
    if("solution"  in reqMap):
        incTicket.solution = reqMap["solution"]
    if("causeAnalysis"  in reqMap):
        incTicket.causeAnalysis = reqMap["causeAnalysis"]
    
    classifier=app.config["CLASSIFIER"]
    cl = app.config["INCIDENTSERVICE"].addNewIncident(incTicket,classifier)
    StatusResult={}
    StatusResult["RESULT"]=cl
    r = Response(json.dumps(StatusResult),  mimetype='application/json')
    
    r.headers['Access-Control-Allow-Origin'] = '*'
    return r

@app.route('/queryIncidentFromLog', methods=['POST'])
def queryIncidentFromLog():
    #check request is a json
    if not request.json:
        abort(400)
    logClassExtractor=app.config["LogClassExtractor"]
    
    reqMap = request.json
    
    logM = LogMessage()
    if ("STATUS" in reqMap.keys() ):
        logM.STATUS = reqMap["STATUS"]
    else:
        abort(402)
    if ("MESSAGE" in reqMap.keys() ):
        logM.MESSAGE = reqMap["MESSAGE"]
    else:
        abort(402)
    if ("ISO_DATE" in reqMap.keys() ):
        logM.ISO_DATE = reqMap["ISO_DATE"]
    else:
        abort(402)
    
    result= logClassExtractor.extractLogClassSolution(logM)
    
    r = Response(json.dumps(result),  mimetype='application/json')
    
    r.headers['Access-Control-Allow-Origin'] = '*'
    return r

@app.route('/<path:path>')
def home(path):
    import os 
    dir_path = os.path.dirname(os.path.realpath(__file__))
    print (dir_path)
    return  send_from_directory('static/', path)

@app.route('/css/<path:path>')
def send_css(path):
    print ('get css')
    return send_from_directory('static/css/', path)

@app.errorhandler(401)
def inCompleteIncident(error):
    return make_response(jsonify({'incident ticket': 'incomplete incidentId and Status'}), 401)

@app.errorhandler(402)
def inCompleteLog(error):
    return make_response(jsonify({'Log ticket': 'incomplete STATUS and MESSAGE'}), 402)

if __name__ == '__main__':
    
    app.run(
        host= '0.0.0.0',
        port=int("8082"),
        debug=True
    )
        