'''
Created on Jan 14, 2017

@author: dexter
'''




import Models.SentenceLabel
from  Models.SentenceModel import Sentence
import numpy as np
import logging
import copy
import json
from pprint import pprint

class ntl_OneNNcluser:
    def __init__(self):
        '''
        Constructor
        '''
        
        self.initialized=False
        self.trainingData=[]
        self.clusterSet={}
        self.distanceThreshold=0.5
        
        
    def initializeCluster(self):
        return
    
    def toMap(self):
        myCopy={}
        myCopy["clusterSet"] = copy.deepcopy(self.clusterSet)
        trainingData=[]
        for s in self.trainingData:
            trainingData.append(s.mystr)
        myCopy["trainingData"] = trainingData
        myCopy["distanceThreshold"]=self.distanceThreshold
        
        return myCopy
    
    def saveModel(self, ModelBackupFile):
        m = self.toMap()
        with open(ModelBackupFile, 'w') as fp:
            json.dump(m, fp)
        return
    
    def loadModel(self, ModelBackupFile):
        
        with open(ModelBackupFile,'r') as fr:
            data = json.load(fr)
        pprint(data)
        
        self.trainingData = []
        
        for s in data["trainingData"]:
            self.trainingData.append(Sentence (s) )
        self.distanceThreshold = data["distanceThreshold"]
        self.clusterSet = data["clusterSet"]
        
        
        
        return
    
    def InsertData(self, data):
        newdata = Sentence(data)
        newdata.init()
        self.trainingData.append(newdata)
        return
    
    def identifyCluster(self, sample):
        clusterName=None
        for cName in self.clusterSet.keys():
            averDist=0
            seedList = self.clusterSet[cName]
            for sd in seedList:
                averDist = averDist + self.trainingData[sd].calculateJaccardDist(sample)
            averDist = averDist / len(seedList)
            logging.debug("Class:"+cName+":"+str(averDist))
            if(averDist<self.distanceThreshold):
                clusterName=cName
                break
        if(clusterName is None):
            #insert the new issue into training sample
            self.trainingData.append(sample)
            inx = self.trainingData.index(sample )
            self.setupNewCluster(inx)
        
        
        return clusterName
    
    def setupNewCluster (self,inx):
        clusterName="C" + str(inx)
        self.clusterSet[ clusterName ] = []
        self.clusterSet[ clusterName ].append(inx)
    
    def buildModelFromTrainingData1D(self):
        #calculate distance
        #"with Jaccord Distance:
        distMatrix = np.zeros(shape=(len(self.trainingData),len(self.trainingData)))
        
        for i in range(0,len(self.trainingData)):
            likeSample=[]
            for j in range (0,i+1):
               #compare the distance in matrix 
               dist = self.trainingData[i].calculateJaccardDist(self.trainingData[j])
               distMatrix[i,j]=dist
               #check dist between sample i and sample j
               if ((i != j) and  (dist < self.distanceThreshold)):
                   likeSample.append(j)
            #check if there is like element
            if(len(likeSample) == 0):
                #create new cluster
                #clusterName="C" + str(i)
                #self.clusterSet[ clusterName ] = []
                #self.clusterSet[ clusterName ].append(i)
                self.setupNewCluster(i)
            else:
                clusterName="C" + str(likeSample[0])
                
                if(clusterName in self.clusterSet):
                    likeSet=self.clusterSet[clusterName]
                    likeSet.append(i)
                
                   
               
        #flip element along the diagional
        fdistMatrix = distMatrix + distMatrix.transpose()
        self.trainingDataMatrix=fdistMatrix
        return fdistMatrix
    
    def printModel(self, fileName):
        fo = open(fileName,'w')

        for i in range(0,len(self.trainingData)):
            fo.write("S"+str(i)+":"+self.trainingData[i].mystr+"\n")
        
        fo.write ("with Jaccord Distance:\n")
        size=len(self.trainingDataMatrix)
        for i in range(0,size):
            for j in range (0, size ):
               fo.write(str(self.trainingDataMatrix[i,j]))
               if( j==size-1):
                   fo.write("")
               else:
                   fo.write(",")
            fo.write("\n")
        
        
        fo.write ("with Cluster:\n")
        clusterNames = self.clusterSet.keys()
        clusterNames.sort()
        for cn in clusterNames:
            fo.write(cn+":")
            for member in self.clusterSet[cn]:
                fo.write(str(member))
                fo.write(",")
            fo.write("\n")
        fo.close()