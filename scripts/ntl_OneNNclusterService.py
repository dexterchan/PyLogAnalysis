'''
Created on Jan 14, 2017

@author: dexter
'''

import os
import sys
from flask import abort
from flask import jsonify
import json
from flask import Flask, request, redirect, send_from_directory,Response
from werkzeug import secure_filename
import logging


from Models.SystemStatus import *
from Classifier.ntl_OneNNcluster import ntl_OneNNcluser 
from logSniffer import *
import argparse
from  Models.SentenceModel import Sentence
# Initialize the Flask application
app = Flask(__name__)


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s (%(threadName)-2s) %(message)s',
                    )

def initialModel(sampleInputFile,oFile,modelFile):
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
    return
parser = argparse.ArgumentParser(__file__, description="NLTK tester")

parser.add_argument("--trainsample", "-s", dest='trainSampleFile', help="Input a training sample file" )
parser.add_argument("--output", "-o", dest='outputFile', help="Write log to output file")
parser.add_argument("--modelfile", "-m", dest='modelfile', help="input by model file")

args = parser.parse_args()
fname=args.trainSampleFile
oFile=args.outputFile
modelFile=args.modelfile
    
fileName="output1DCluster.txt"
if (oFile is None):
        oFile=fileName
#if ( fname is None):
#        logging.error("No initial error log sample file in parameter --input")
        
initialModel(fname,oFile,modelFile)


@app.route('/submitlog', methods=['POST'])
def submitLog():
    #check request is a json
    if not request.json:
        abort(400)
    classifier=app.config["CLASSIFIER"]
    
    reqMap = request.json
    newdata = Sentence(reqMap["MESSAGE"])
    newdata.init()
    
    cName=classifier.identifyCluster(newdata)
    StatusResult={}
    if(cName is not None):
        StatusResult["found"]=True
        StatusResult["cluster"]=cName
    else:
        StatusResult["found"]=False
        StatusResult["cluster"]="NoClass"
    
    return Response(json.dumps(StatusResult),  mimetype='application/json')
    #return jsonify({'ret': LogAnalyzeStatus}), 201


if __name__ == '__main__':
    
    app.run(
        host= '0.0.0.0',
        port=int("8082"),
        debug=True
    )
        