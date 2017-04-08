'''
Created on Apr 8, 2017

@author: dexter
'''
from ProcessQueue.LogProcess import  *

from ProcessQueue.LogPublisher import  *

p=RestfulPublisher("http://ec2-54-208-51-43.compute-1.amazonaws.com:8082/queryIncidentFromLog")

data = {}

data["ISO_DATE"] = "2016-12-30 16:27:54,435"
data["MESSAGE"]= "FxRestfulController: USDUSD not found: ccy1 and ccy2 should not be the same FxRestfulController.java 208 "
data["STATUS"]="OK"

(response,content)=p.publish(data)

print(response)
print(content)
