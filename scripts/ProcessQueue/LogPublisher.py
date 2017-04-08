'''
Created on Apr 8, 2017

@author: dexter
'''
import httplib2
import json
import time
import datetime

class RestfulPublisher():
    def __init__(self, URL):
        self.URL = URL
        
        self.http=httplib2.Http()
        content_type_header="application/json"
        self.headers = {'Content-Type': content_type_header}
        return
    
    def publish(self, data):
        
        response, content = self.http.request( self.URL,'POST',json.dumps(data),headers=self.headers)
        return (response,content)