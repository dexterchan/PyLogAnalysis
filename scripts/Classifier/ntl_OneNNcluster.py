'''
Created on Jan 14, 2017

@author: dexter
'''




import Models.SentenceLabel
from  Models.SentenceModel import Sentence
import numpy as np
import logging
class ntl_OneNNcluser:
    def __init__(self, trainingDataFile):
        '''
        Constructor
        '''
        
        self.initialized=False
        self.trainingData=[]
        self.clusterSet={}
        self.distanceThreshold=0.5
        
        
    def initializeCluster(self):
        return
    
    def initializeModelFromTrainingDataFile(self, trainingDataFile):
        
        
        
        
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
        
        return clusterName
    
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
                clusterName="C" + str(i)
                self.clusterSet[ clusterName ] = []
                self.clusterSet[ clusterName ].append(i)
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