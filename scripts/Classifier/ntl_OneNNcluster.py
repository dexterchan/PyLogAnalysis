'''
Created on Jan 14, 2017

@author: dexter
'''




import Models.SentenceLabel
from  Models.SentenceModel import Sentence
import numpy as np
class ntl_OneNNcluser:
    def __init__(self, trainingDataFile):
        '''
        Constructor
        '''
        
        self.initialized=False
        self.trainingData=[]
        
    def initializeCluster(self):
        return
    
    def initializeModelFromTrainingDataFile(self, trainingDataFile):
        
        
        
        
        return
    
    def InsertData(self, data):
        newdata = Sentence(data)
        newdata.init()
        self.trainingData.append(newdata)
        return
    
    def buildModelFromTrainingData1D(self):
        #calculate distance
        #"with Jaccord Distance:
        distMatrix = np.zeros(shape=(len(self.trainingData),len(self.trainingData)))
        
        for i in range(0,len(self.trainingData)):
            for j in range (0,i+1):
               #compare the distance in matrix 
               dist = self.trainingData[i].calculateJaccardDist(self.trainingData[j])
               distMatrix[i,j]=dist
        #flip element along the diagional
        fdistMatrix = distMatrix + distMatrix.transpose()
        return fdistMatrix