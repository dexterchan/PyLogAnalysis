'''
Created on Jan 14, 2017

@author: dexter
'''
from Classifier.ntl_OneNNcluster import ntl_OneNNcluser 

def testSentenceDataInsert():
    classifier = ntl_OneNNcluser("file.txt")
    classifier.InsertData("ERROR 2016-12-31 18:39:40,268 - FxRestfulController: JPYJPY not found: ccy1 and ccy2 should not be the same FxRestfulController.java 64 ")
    classifier.InsertData('ERROR 2016-12-30 16:27:54,435 - FxRateUpdaterThread: org.springframework.web.client.ResourceAccessException: I/O error on GET request for "http://www.apilayer.ne/api/live": www.apilayer.ne: nodename nor servname provided, or not known; nested exception is java.net.UnknownHostException: www.apilayer.ne: nodename nor servname provided, or not known FxRateUpdaterThread.java 88')
    
    m=classifier.buildModelFromTrainingData1D()
    print (m) 
    return


testSentenceDataInsert()

